#!/usr/bin/env python
"""
Repo commits application.

Fetch commits for a given repo and optional start date.
"""
import math
import sys

import lib
import lib.git

QUERY_PATH = 'queries/repos/repo_commits.gql'


def get_commits(variables):
    # TODO: Validate for specific keys.
    results = []
    counter = 0

    repo_name = variables['name']
    branch_name = None

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


def main(args):
    """
    Main command-line function.
    """
    if not args or set(args).intersection({'-h', '--help'}):
        print(
            f"Usage: {__file__} owner OWNER name REPO_NAME [start START_DATE]")
        print(f"START_DATE: Count commits on or after this date, in YYYY-MM-DD format.")
        sys.exit(1)

    variables = lib.process_variables(args)
    get_commits(variables)


if __name__ == '__main__':
    main(sys.argv[1:])
