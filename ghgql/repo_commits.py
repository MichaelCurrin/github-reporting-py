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
CSV_OUT_NAME = 'repo-commits--{repo_name}--start-{start}--end-{end}.csv'


def get_commits(owner, repo_name, start=None):
    """
    Fetch all commits for a given repo and optional start date.

    Uses paging if there is more than 1 page of 100 commits to fetch.
    Returns a list of zero or more dict objects with commit data.
    """
    results = []

    branch_name = None
    since = lib.time.timestamp(start) if start else None

    variables = dict(
        owner=owner,
        repo_name=repo_name,
        since=since,
    )

    counter = 0
    while True:
        counter += 1

        resp = lib.query_by_filename(QUERY_PATH, variables)

        repo_data = resp['repository']

        branch = repo_data['defaultBranchRef']
        if not branch_name:
            branch_name = branch.get('name')

        commit_history = branch['target']['history']
        if not variables.get('cursor', None):
            print("Expected")
            print(f" - commits: {commit_history['totalCount']}")
            print(f" - pages: {math.ceil(commit_history['totalCount'] / 100)}")

        raw_commits = branch['target']['history']['nodes']
        commits = [lib.git.prepare_row(c, repo_name, branch_name) for c in
                   raw_commits]
        results.extend(commits)

        print(f"Processed page: #{counter}")

        page_info = commit_history['pageInfo']
        if page_info['hasNextPage']:
            variables['cursor'] = page_info['endCursor']
        else:
            break

    return results


def main():
    """
    Main command-line function.
    """
    parser = argparse.ArgumentParser("Repo commits report")

    parser.add_argument(
        'owner',
        metavar="OWNER"
    )
    parser.add_argument(
        'repo_name',
        metavar="REPO_NAME"
    )
    parser.add_argument(
        '-s', '--start',
        metavar="DATE",
        help="Optionally filter to commits from this date"
        " onwards. format 'YYYY-MM-DD'."
    )

    args = parser.parse_args()

    repo_commits = get_commits(args.owner, args.repo_name, args.start)
    path = lib.VAR_DIR / CSV_OUT_NAME.format(
        repo_name=args.repo_name,
        start=args.start if args.start else "INIT",
        end=datetime.date.today()
    )
    lib.write_csv(path, repo_commits, append=False)


if __name__ == '__main__':
    main()
