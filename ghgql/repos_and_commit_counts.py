#!/usr/bin/env python
"""
Repo commit counts - report application.

Generate a report which shows all repos under an owner and a total commit count
against each, using the default branch. Optionally exclude commits after a given
start date.

This script uses paging to get each page of repos.
"""
import math
import sys

import lib.text


ITEMS_PER_PAGE = 100
QUERY_PATH = 'queries/repos/repos_and_commit_counts.gql'


@lib.text.print_args_on_error
def format_repo(repo) -> dict:
    """
    Format summary repo data and return as key-value pairs,
    """
    branch = repo.get('defaultBranch')

    # Handle case of an empty repo.
    branch_name = None
    total_commits = 0
    last_committed_date = None
    last_commit_msg_subject = None

    if branch:
        branch_name = branch['name']
        history = branch['commits']['history']
        total_commits = history['totalCount']

        if total_commits:
            latest_commit = history['nodes'][0]
            last_committed_date = lib.time.as_date(
                latest_commit['committedDate'])
            # TODO: Check this.
            last_commit_msg_subject = latest_commit['message'].split("\n")[0]

    return dict(
        owner_name=repo['owner']['login'],
        repo_name=repo['name'],
        branch_name=branch_name,
        total_commits=total_commits,
        last_committed_date=last_committed_date,
        last_commit_msg_subject=last_commit_msg_subject,
    )


def get_repos_and_commit_counts(path, variables) -> list:
    """
    Get commit counts for all repos owned by an account.

    :return out_repos: list where each item contains a dict of repo info.
    """
    print("Fetching repos and commit counts")
    out_repos = []

    count = 0
    while True:
        count += 1
        print(f"Query #{count}")

        resp_data = lib.query_by_filename(path, variables)
        fetched_repos = resp_data['repositoryOwner']['repositories']

        if count == 1:
            grand_total = fetched_repos['totalCount']
            print("Completed first page.")
            print("Data to fetch:")
            print(f" - repos: {grand_total:,d}")
            print(f" - pages: {math.ceil(grand_total/ITEMS_PER_PAGE):,d}")

        for repo in fetched_repos['nodes']:
            formatted_repo_data = format_repo(repo)
            out_repos.append(formatted_repo_data)

        repo_page_info = fetched_repos['pageInfo']
        if repo_page_info['hasNextPage']:
            variables['cursor'] = repo_page_info['endCursor']
        else:
            break

    return out_repos


def counts_report(variables):
    out_data = get_repos_and_commit_counts(QUERY_PATH, variables)
    lib.write_csv(lib.COUNTS_CSV_PATH_TODAY, out_data)


def main(args):
    """
    Main command-line function.
    """
    if not args or set(args).intersection({'-h', '--help'}):
        print(f"Usage: {__file__} owner OWNER [start START_DATE]")
        print("START_DATE: Count commits on or after this date, in YYYY-MM-DD"
              " format. This only affects the commit count and not whether the"
              " repo is shown.")
        sys.exit(1)

    variables = lib.process_variables(args)
    counts_report(variables)


if __name__ == '__main__':
    main(sys.argv[1:])
