"""
Repo commits application.

Fetch commits for a given repo and optional start date.
"""
import sys

import lib
import lib.git

QUERY_PATH = 'queries/repos/repo_commits.gql'


def process_commits(raw_commits, name, branch_name):
    output_data = []
    for c in raw_commits:
        parsed_commit_data = lib.git.parse_commit(c)
        out_commit = dict(
            repo_name=name,
            branch_name=branch_name,
            **parsed_commit_data,
        )
        output_data.append(out_commit)

    return output_data


def get_commits(variables):
    # TODO: Validte for specific keys.
    name = variables['name']

    resp = lib.query_by_filename(QUERY_PATH, variables)
    repo_data = resp['repository']

    branch = repo_data['defaultBranchRef']
    branch_name = branch.get('name')

    commit_history = branch['target']['history']
    total_count = commit_history['totalCount']

    raw_commits = branch['target']['history']['nodes']
    commits = process_commits(raw_commits, name, branch_name)

    page_info = repo_data['defaultBranchRef']['target']['history']['pageInfo']

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
    print(get_commits(variables))


if __name__ == '__main__':
    main(sys.argv[1:])
