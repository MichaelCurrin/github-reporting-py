#!/usr/bin/env python
"""
Repo commits application.

Fetch commits for a given repo and optional start date.
"""
import argparse
import datetime
import math

import lib
import lib.git


QUERY_PATH = 'queries/repos/repo_commits.gql'
CSV_OUT_NAME = 'repo-commits--{repo_name}--end-{end_date}--start-{start_date}.csv'


def process_response(resp, repo_name):
    """
    Format response for a request of repo commits
    """
    branch = resp['repository']['defaultBranchRef']

    branch_name = branch.get('name')

    commit_history = branch['target']['history']
    commits = [lib.git.prepare_row(c, repo_name, branch_name)
               for c in commit_history['nodes']]
    total_commits = commit_history['totalCount']

    page_info = commit_history['pageInfo']
    cursor = page_info['endCursor'] if page_info['hasNextPage'] else None

    return commits, total_commits, cursor


def get_commits(owner, repo_name, start_date=None):
    """
    Fetch all commits for a given repo and optional start date.

    Uses paging if there is more than 1 page of 100 commits to fetch. Returns a
    list of zero or more dict objects with commit data.
    """
    print("/".join((owner, repo_name)))

    since = lib.time.as_git_timestamp(start_date) if start_date else None

    query_variables = dict(
        owner=owner,
        repo_name=repo_name,
        since=since,
    )

    results = []

    counter = 0
    while True:
        counter += 1

        resp = lib.query_by_filename(QUERY_PATH, query_variables)
        commits, total_commits, cursor = process_response(resp, repo_name)

        if counter == 1:
            print(f" - commits: {total_commits}")
            print(f" - pages: {math.ceil(total_commits / 100)}")

        results.extend(commits)
        print(f"Processed page: #{counter}")

        if cursor:
            query_variables['cursor'] = cursor
        else:
            break

    return results


def commits_to_csv(owner, repo_name, start_date=None):
    """
    Write a CSV of all commits in a repo.

    Existing file will be overwritten.
    """
    repo_commits = get_commits(owner, repo_name, start_date)
    filename = CSV_OUT_NAME.format(
        repo_name=repo_name,
        end_date=datetime.date.today(),
        start_date=start_date if start_date else "INIT",
    )
    path = lib.VAR_DIR / filename
    lib.write_csv(path, repo_commits, append=False)


def main():
    """
    Main command-line function.
    """
    parser = argparse.ArgumentParser(description="Repo commits report")

    parser.add_argument(
        'owner',
        metavar="OWNER",
    )
    parser.add_argument(
        'repo_name',
        metavar="REPO_NAME",
    )
    parser.add_argument(
        '-s', '--start',
        metavar="DATE",
        help="Optionally filter to commits from this date onwards."
            " Format: 'YYYY-MM-DD'.",
    )

    args = parser.parse_args()
    commits_to_csv(
        args.owner,
        args.repo_name,
        args.start,
    )


if __name__ == '__main__':
    main()
