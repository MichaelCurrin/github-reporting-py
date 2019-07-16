"""
Repo commit counts report application.

Process a query which supports paging and contains repo commits and iterates
over all the pages. Get all repos owned by user and print the count of commits
on the default branch in each repo. An optional start date cutoff may be
specified.
"""
import datetime
import sys
import textwrap

import lib


def main(args):
    """
    Main command-line function.
    """
    if not args or set(args).intersection({'-h', '--help'}):
        print(f"Usage: {__file__} login LOGIN [start START_DATE]")
        print(f"START_DATE: Count commits on or after this date, in YYYY-MM-DD format.")
        sys.exit(1)

    path = 'queries/paged/repos_and_commit_counts.gql'
    variables = lib.process_variables(args)
    start = variables.pop('start', None)
    if start:
        variables['since'] = datetime.datetime.strptime(start, '%Y-%m-%d').isoformat()

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
                print(f"Name         : {repo_name}")

                branch = repo.get('defaultBranch')
                if branch:
                    branch_name = branch['name']
                    history = branch['commits']['history']
                    total_commits = history['totalCount']

                    if total_commits:
                        print(f"Branch       : {branch_name}")
                        print(f"Commits      : {total_commits:,d}")
                        latest_commit = history['nodes'][0]

                        date = latest_commit['committedDate'][:10]
                        msg = latest_commit['message']

                        print(f"Latest commit:")
                        print(f"  {date}")
                        print(textwrap.indent(msg, '  '))
                    print()
                else:
                    # Handle rare cases of an empty repo.
                    print(f"No branch or commit data")
            except Exception:
                print(repo)
                raise

        repo_page_info = repositories['pageInfo']
        if repo_page_info['hasNextPage']:
            variables['cursor'] = repo_page_info['endCursor']
        else:
            break


if __name__ == '__main__':
    main(sys.argv[1:])