#!/usr/bin/env python
"""
Repo commits report application.

Fetch all commits for a single given repo using paging. Accepts an optional
committer, output dir, start date, end date, and verbosity.
"""
import argparse
import datetime
import math
from pathlib import Path

import lib
import lib.git

QUERY_PATH = Path("queries/repos/repo_commits.gql")
QUERY_PATH_BRANCH = Path("queries/repos/repo_commits_branch.gql")

CSV_OUT_NAME = "{owner}--{repo}--start-{start}--end-{end}.csv"
CSV_OUT_NAME_BRANCH = "{owner}--{repo}--{branch}--start-{start}--end-{end}.csv"


def parse(resp: dict, branch_name):
    """
    Parse response data for the repo commits query.
    """
    key = "ref" if branch_name else "defaultBranchRef"
    branch = resp["repository"][key]
    branch_name = branch.get("name")
    commit_history = branch["target"]["history"]
    total_commits = commit_history["totalCount"]
    commits = commit_history["nodes"]
    page_info = commit_history["pageInfo"]
    cursor = page_info["endCursor"] if page_info["hasNextPage"] else None

    return branch_name, total_commits, commits, cursor


def process_response(resp: dict, repo_name: str, branch_name: str, verbose=False):
    """
    Format the response from a request for repo commits.
    """
    branch_name, total_commits, commits, cursor = parse(resp, branch_name)
    processed_commits = [
        lib.git.prepare_row(c, repo_name, branch_name, verbose) for c in commits
    ]

    return processed_commits, total_commits, cursor


def get_commits(
        owner: str,
        repo_name: str,
        branch_name=None,
        committer=None,
        start_date=None,
        end_date=None,
        verbose=False) -> list[dict]:
    """
    Fetch all commits for a given repo and  an optional start date.

    Uses paging if there is more than 1 page of 100 commits to fetch. Returns a
    list of zero or more dict objects with commit data.
    """
    if branch_name:
        print("/".join((owner, repo_name, branch_name)))
    else:
        print("/".join((owner, repo_name)))

    since = lib.time.as_git_timestamp(start_date) if start_date else None
    before = lib.time.as_git_timestamp(end_date) if end_date else None
    query_variables = dict(
        owner=owner,
        repo_name=repo_name,
        branch_name=branch_name,
        since=since,
    )

    results = []
    counter = 0

    while True:
        counter += 1

        query_path = QUERY_PATH_BRANCH if branch_name else QUERY_PATH
        resp = lib.query_by_filename(query_path, query_variables)
        commits, _, cursor = process_response(resp, repo_name, branch_name, verbose)
        results.extend(commits)

        if cursor:
            query_variables["cursor"] = cursor
        else:
            break

    if committer:
        results = list(filter(
            lambda res: res["committer_login"] == committer,
            results
        ))

    if before:
        before = lib.time.as_date(before)
        results = list(filter(
            lambda res: res["committed_date"] < before,
            results
        ))

    if counter == 1:
        total_commits = len(results)
        print(f" - commits: {total_commits}")
        print(f" - pages: {math.ceil(total_commits / 100)}")
        print(f"Processed page: #{counter}")

    return results


def commits_to_csv(
        owner,
        repo_name,
        branch_name=None,
        committer=None,
        output_dir=None,
        start_date="START",
        end_date=datetime.date.today(),
        verbose=False):
    """
    Write a CSV of all commits in a repo.

    Existing file will be overwritten.
    """
    filename = CSV_OUT_NAME_BRANCH if branch_name else CSV_OUT_NAME
    filename = filename.format(
        owner=owner,
        repo=repo_name,
        branch=branch_name,
        start=start_date,
        end=end_date,
    )
    output_dir = Path(output_dir) if output_dir else lib.VAR_DIR
    path = output_dir / filename
    repo_commits = get_commits(
        owner,
        repo_name,
        branch_name,
        committer,
        start_date,
        end_date,
        verbose,
    )

    lib.write_csv(path, repo_commits, append=False)


def main():
    """
    Main command-line function.
    """
    parser = argparse.ArgumentParser(description="Repo commits report")

    parser.add_argument(
        "owner",
        metavar="OWNER",
        help="Owner of the repository."
    )
    parser.add_argument(
        "repo",
        metavar="REPO",
        help="Repository name."
    )
    parser.add_argument(
        "committer",
        metavar="COMMITTER",
        help="Username of the commit author."
    )
    parser.add_argument(
        "-b",
        "--branch",
        metavar="BRANCH",
        help="Specific branch to pull commits from.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        metavar="DIR",
        help="Directory in which to write the csv file.",
    )
    parser.add_argument(
        "-s",
        "--start",
        metavar="DATE",
        help="Optionally filter to commits from this date onwards."
        " Format: 'YYYY-MM-DD'.",
    )
    parser.add_argument(
        "-e",
        "--end",
        metavar="DATE",
        help="Optionally filter to commits strictly before this date."
        " Format: 'YYYY-MM-DD'.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Verbose commit output.",
    )

    args = parser.parse_args()
    commits_to_csv(
        args.owner,
        args.repo,
        args.branch,
        args.committer,
        args.output_dir,
        args.start,
        args.end,
        args.verbose,
    )


if __name__ == "__main__":
    main()
