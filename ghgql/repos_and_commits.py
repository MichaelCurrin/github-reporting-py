"""
Repos and commits report.

For a given repo owner and option start data, get all commits for all repos
under that the owner.

While paging of either repos or commits is possible, it is not possible in the
API handle the outer and inner paging at the same time. So the approach here is
to build up a list of repos to query and using paging and a cursor for each to
get their commits. When there is nothing to get from a repo, it falls away and
can be replaced by another. Note that the total number of repos should not be so
high that the request fails. Querying 100 repos (and 100 commits each) is very
likely to fail based on tests, therefore a lower count is used.

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
from collections import defaultdict

import lib


TEMPLATE_DIR = lib.APP_DIR / 'templates'
QUERY_PATH = TEMPLATE_DIR / 'repos_and_commits.gql'
# TODO: Var from config.
CSV_PATH = lib.APP_DIR / 'var' / 'commits.csv'


def render(template, owner, repos, since, dry_run=False):
    """
    Prepare and return template for repo commits query.
    """
    return template.render(
        owner=owner,
        repos=repos,
        since=since,
        dry_run=dry_run
    )


def parse_commit(value):
    """
    Extract fields from nested data as returned from API and return as flat dict.
    """
    author = value['committer']['user']
    author_login = author['login'] if author is not None else None
    author_date = lib.as_date(value['authoredDate'])

    committer = value['committer']['user']
    committer_login = committer['login'] if committer is not None else None
    commit_date = lib.as_date(value['committedDate'])

    return dict(
        commit_id=value['abbreviatedOid'],
        author_date=author_date,
        author_login=author_login,

        commited_date=commit_date,
        commiter_login=committer_login,

        changed_files=value['changedFiles'],
        additions=value['additions'],
        deletions=value['deletions'],
        message=value['message'],
    )


def write(path, rows):
    wrote_header = False

    with open(path, 'w') as f_out:
        fieldnames = None

        for repo_title, commits in rows.items():
            print(repo_title)
            if not fieldnames:
                fieldnames = commits[0].keys()
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            if not wrote_header:
                writer.writeheader()
                wrote_header = True
            writer.writerows(commits)

    print(f"Wrote: {path}")


def main():
    """
    Main command-line function.
    """
    since_input = '2019-08-01'

    since = lib.timestamp(since_input) if since_input else None
    owner = 'michaelcurrin'
    repo_names = ['twitterverse', 'docsify-template']

    repos = [{'name': name, 'cursor': None} for name in repo_names]

    template = lib.read_template(QUERY_PATH)
    # Response if key-value pairs where the key has to be unique for the query
    # but is not needed when parsing results.
    query = render(template, owner, repos, since)
    results = lib.fetch_github_data(query)
    rate_limit = results.pop('rateLimit')

    # TODO: Clear a repo when it has been finished and write to disc, so that
    # is known in the CSV to the last success.
    output_data = defaultdict(list)
    for repo_data in results.values():
        name = repo_data['name']
        branch = repo_data['defaultBranchRef']
        branch_name = branch['name']

        raw_commits = branch['target']['history']['nodes']
        if raw_commits:
            for c in raw_commits:
                parsed_commit_data = parse_commit(c)
                out_commit = dict(
                    repo_name=name,
                    branch_name=branch_name,
                    **parsed_commit_data,
                )
                output_data[name].append(out_commit)
        # else it is exhausted so can be removed

        page_info = repo_data['defaultBranchRef']['target']['history']['pageInfo']

    write(CSV_PATH, output_data)


if __name__ == '__main__':
    main()
