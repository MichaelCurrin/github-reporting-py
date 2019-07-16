"""
Pagination application.

Process a query which supports paging and contains repo commits and iterates
over all the pages.

This only works with a query with returns output in a specific format.
"""
import sys

import lib


def main(args):
    """
    Main command-line function.
    """
    if len(args) != 2 or set(args).intersection({'-h', '--help'}):
        print(f"Usage: {__file__}")
        sys.exit(1)

    path = 'queries/paged/commit_count_by_repo.gql'
    variables = lib.process_variables(args)

    first_iteration = True
    while True:
        data = lib.query_by_filename(path, variables)

        repositories = data['repositoryOwner']['repositories']
        if first_iteration:
            print(f"Total count: {repositories['totalCount']}")
            first_iteration = False

        for repo in repositories['nodes']:
            try:
                repo_name = repo['name']
                print(f"Name   : {repo_name}")

                branch = repo.get('defaultBranch')
                if branch:
                    branch_name = branch['name']
                    history = branch['commits']['history']
                    total_commits = history['totalCount']
                    commits = history['nodes']
                    latest_commit = commits[0]

                    date = latest_commit['committedDate'][:10]
                    msg = latest_commit['message']

                    print(f"Branch : {branch_name}")
                    print(f"Commits: {total_commits:,d}")
                    print(f"Latest commit:")
                    print(f"  Date   : {date}")
                    print(f"  Message:")
                    print(msg)
                    print()
                else:
                    print(f"Not branch or commit data")
            except Exception:
                print(repo)
                raise

        repo_page_info = repositories['pageInfo']
        if repo_page_info['hasNextPage']:
            variables['after'] = repo_page_info['endCursor']
        else:
            break


if __name__ == '__main__':
    main(sys.argv[1:])
