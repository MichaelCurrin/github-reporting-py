#!/usr/bin/env python
"""
Report for commits of repos.

NOTE: This is an experimental script that has performance issues.

For a given repo owner and option start data, get all commits for all repos
under that the owner.

While paging of either repos or commits is possible, it is not possible in the
API handle the outer and inner paging at the same time. So the approach here is
to build up a list of repos to query and using paging and a cursor for each to
get their commits. When there is nothing to get from a repo, it falls away and
can be replaced by another. Note that the total number of repos should not be so
high that the request fails. Querying 100 repos (and 100 commits each) is very
likely to fail based on tests, therefore a lower count is used. If efficiency
is not important, rather use the Repos About query's list of repo names and then
run a report against each repo sequentially.

Jinja templating is used to build up the GQL query neatly.

The GQL "fragment" syntax is used in order to limit the total size of the query
text, as the long list of fields needed for each repo is defined once in the
fragment.

Note that no JSON data is supplied in the request. Since a fragment cannot
accept arguments. It was not tested yet whether a fragment can get the "global"
arguments. But since the whole query is built from scratch on each request based
on required repos, it is easy to substitute in values that would normally be in
the JSON data payload like "owner".
"""
import csv
import sys
from collections import defaultdict

import read_counts
import lib.git
import lib.text


TEMPLATE_DIR = lib.APP_DIR / "templates"
QUERY_PATH = TEMPLATE_DIR / "repos_and_commits.gql"
CSV_PATH = lib.VAR_DIR / "commits.csv"


def render(template, owner, repos, since, dry_run=False):
    """
    Prepare and return template for repo commits query.
    """
    return template.render(owner=owner, repos=repos, since=since, dry_run=dry_run)


def process_results(results):
    """
    :param results: dict where each key is a repo name or a metadata field.

    :return output_data:
    """
    rate_limit = results.pop("rateLimit")

    # TODO: Clear a repo when it has been finished and write to disc, so that
    # is known in the CSV to the last success.
    output_data = defaultdict(list)
    for repo_data in results.values():
        name = repo_data["name"]
        branch = repo_data["defaultBranchRef"]

        branch_name = branch.get("name")

        raw_commits = branch["target"]["history"]["nodes"]
        if raw_commits:
            for c in raw_commits:
                parsed_commit_data = lib.git.parse_commit(c)
                out_commit = dict(
                    repo_name=name,
                    branch_name=branch_name,
                    **parsed_commit_data,
                )
                output_data[name].append(out_commit)
        # else it is exhausted so can be removed

        # TODO: Use.
        page_info = repo_data["defaultBranchRef"]["target"]["history"]["pageInfo"]
        print(page_info)

    return output_data, rate_limit


def get_results(template, owner, repos, since, dry_run):
    """
    Fetch commit data using parameters and template and return parsed results.

    Response if key-value pairs where the key has to be unique for the query
    but is not needed when parsing results.
    """
    query = render(template, owner, repos, since, dry_run)
    results = lib.fetch_github_data(query)

    return process_results(results)


def write(path, rows):
    wrote_header = False

    with open(path, "w") as f_out:
        fieldnames = (
            "repo_name",
            "branch_name",
            "commit_id",
            "author_date",
            "author_login",
            "committed_date",
            "committer_login",
            "changed_files",
            "additions",
            "deletions",
            "message",
        )

        for repo_title, commits in rows.items():
            print(f"{repo_title:20}| {len(commits):5,d}")

            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            if not wrote_header:
                writer.writeheader()
                wrote_header = True
            writer.writerows(commits)

    print(f"Wrote: {path}")


def do_query(template, owner, repos, since, dry_run):
    """
    Fetch, parse and write commits for a batch of commits.

    The number of commits returned for each repo cannot be more than 100 in
    a single request, because of pagination in the API.
    """
    out_data, rate_limit = get_results(template, owner, repos, since, dry_run)
    print(lib.text.prettify(rate_limit))

    write(CSV_PATH, out_data)


def clean(name):
    """
    Prepare name for query.

    Remove numeric characters which cause the query to break if at the start.
    """
    name = name.replace("-", "_").replace(".", "X")

    if name[0].isnumeric():
        name = f"X{name[1:]}"

    return name


def make_report(owner, repo_names, since, dry_run=False):
    """
    Fetch commit data for all named repos, using multiple queries.

    Data is written out after each request.
    TODO: Write data when there are no more commits for a repo.
    TODO: Write header.
    TODO: Single single CSV writer and pass it around or are the context block issues?
    """
    template = lib.read_template(QUERY_PATH)

    # TODO: Split in batches.
    repo_names = repo_names[:30]
    repos = [
        {"name": name, "clean_name": clean(name), "cursor": None} for name in repo_names
    ]

    print("Query #1")
    do_query(template, owner, repos, since, dry_run)


def main(args):
    """
    Main command-line function.
    """
    if not args or set(args).intersection({"-h", "--help"}):
        print(f"Usage: {__file__} owner OWNER [start START_DATE]")
        print(f"START_DATE: Count commits on or after this date, in YYYY-MM-DD format.")
        sys.exit(1)

    variables = lib.process_variables(args)
    start = variables.get("start", None)

    start_ts = lib.time.as_git_timestamp(start) if start else None
    owner_name, repo_names = read_counts.repo_names(start)

    make_report(owner_name, repo_names, start_ts, dry_run=False)


if __name__ == "__main__":
    main(sys.argv[1:])
