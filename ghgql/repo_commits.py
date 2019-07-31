"""
Repo commits application.
"""
import sys

import lib


def get_commits(path, variables):
    # TODO Only need to print or retrieve branch name on first query.
    # TODO Add paging
    # TODO Add return
    resp_data = lib.query_by_filename(path, variables)
    branch = resp_data['repository']['defaultBranchRef']
    branch_name = branch['name']
    commit_history = branch['target']['history']
    total = commit_history['totalCount']
    commits = commit_history['nodes']
    print(branch_name)
    print(total)

    for c in commits:
        print(c)


def main(args):
    """
    Main command-line function.
    """
    if not args or set(args).intersection({'-h', '--help'}):
        print(f"Usage: {__file__} owner OWNER name REPO_NAME [start START_DATE]")
        print(f"START_DATE: Count commits on or after this date, in YYYY-MM-DD format.")
        sys.exit(1)

    path = 'queries/repos/repo_commits.gql'
    variables = lib.process_variables(args)
    get_commits(path, variables)


if __name__ == '__main__':
    main(sys.argv[1:])
