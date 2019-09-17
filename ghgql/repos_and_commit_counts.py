"""
Repo commit counts report application.

Process a query which supports paging and contains repo commits and iterates
over all the pages. Get all repos owned by user and the count of commits
on the default branch in each repo. An optional start date cutoff may be
specified.

The data is formatted and written out to a CSV report.
"""
import math
import sys

import lib.text


ITEMS_PER_PAGE = 100


@lib.text.print_args_on_error
def format_repo(repo):
    """
    Format summary repo data and return as dict.
    """
    branch = repo.get('defaultBranch')
    if branch:
        branch_name = branch['name']
        history = branch['commits']['history']
        total_commits = history['totalCount']

        if total_commits:
            latest_commit = history['nodes'][0]
            last_committed_date = lib.time.as_date(latest_commit['committedDate'])
            last_commit_msg_subject = latest_commit['message'].split("\n")[0]
    else:
        # Handle case of an empty repo.
        branch_name = None
        total_commits = 0
        last_committed_date = None
        last_commit_msg_subject = None

    return dict(
        repo_name=repo['name'],
        branch_name=branch_name,
        total_commits=total_commits,
        last_committed_date=last_committed_date,
        last_commit_msg_subject=last_commit_msg_subject,
    )


def get_repos_and_commit_counts(path, variables):
    """
    Get commit counts for all repos owned by an account.

    :return: dict
    """
    first_iteration = True

    repo_data = []

    print("Fetching repos and commit counts")

    count = 0
    while True:
        count += 1
        print(f"Query #{count}")

        resp_data = lib.query_by_filename(path, variables)
        repositories = resp_data['repositoryOwner']['repositories']

        if first_iteration:
            grand_total = repositories['totalCount']
            print("Completed first page.")
            print("Data to fetch:")
            print(f" - repos: {grand_total:,d}")
            print(f" - pages: {math.ceil(grand_total/ITEMS_PER_PAGE):,d}")
            first_iteration = False

        for repo in repositories['nodes']:
            formatted_repo_data = format_repo(repo)
            repo_data.append(formatted_repo_data)

        repo_page_info = repositories['pageInfo']
        if repo_page_info['hasNextPage']:
            variables['cursor'] = repo_page_info['endCursor']
        else:
            break

    return repo_data


def main(args):
    """
    Main command-line function.
    """
    if not args or set(args).intersection({'-h', '--help'}):
        print(f"Usage: {__file__} owner OWNER [start START_DATE]")
        print(f"START_DATE: Count commits on or after this date, in YYYY-MM-DD format.")
        sys.exit(1)

    path = 'queries/repos/repos_and_commit_counts.gql'
    variables = lib.process_variables(args)
    out_data = get_repos_and_commit_counts(path, variables)

    lib.write_csv(lib.COUNTS_CSV_PATH, out_data)


if __name__ == '__main__':
    main(sys.argv[1:])
