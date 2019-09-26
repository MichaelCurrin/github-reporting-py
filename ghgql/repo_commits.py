#!/usr/bin/env python
"""
Repo commits application.

Fetch commits for a given repo and optional start date.
"""
import argparse
import math

import lib
import lib.git

QUERY_PATH = 'queries/repos/repo_commits.gql'


def get_commits(owner, repo_name, since=None):
    results = []
    counter = 0

    branch_name = None

    variables = dict(
        owner=owner,
        repo_name=repo_name,
        since=since,
    )
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

    return commits


def main():
    """
    Main command-line function.
    """
    parser = argparse.ArgumentParser("Repo commits report")

    parser.add_argument('owner',
                        metavar="OWNER")
    parser.add_argument('repo_name',
                        metavar="REPO_NAME")
    parser.add_argument('-s', '--start',
                        metavar="YYYY-MM-DD")

    args = parser.parse_args()
    if args.start:
        args.start = lib.time.timestamp(args.start)

    get_commits(args.owner, args.repo_name, args.start)


if __name__ == '__main__':
    main()
