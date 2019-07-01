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
    if not args or set(args).intersection({'-h', '--help'}):
        print(f"Usage: {__file__}")
        sys.exit(1)

    path, variables = lib.process_args(args)

    first_iteration = True
    while True:
        data = lib.query_by_filename(path, variables)

        repositories = data['repositoryOwner']['repositories']
        if first_iteration:
            print(f"Total count: {repositories['totalCount']}")
            first_iteration = False

        for repo in repositories['nodes']:
            latest_commit = repo['defaultBranch']['commits']['history']['latest']
            print(lib.prettify(latest_commit))

        repo_page_info = repositories['pageInfo']
        if repo_page_info['hasNextPage']:
            variables['after'] = repo_page_info['endCursor']
        else:
            break


if __name__ == '__main__':
    main(sys.argv[1:])
