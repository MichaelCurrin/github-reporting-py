#!/usr/bin/env python
"""
Repo commits from config report application.
"""
import argparse
import datetime

import lib
import lib.text
import repo_commits
from config import COMMIT_REPORT_CONF


CSV_OUT_NAME = 'repos-commits--configured--end-{end_date}--start-{start_date}.csv'


def report_config():
    owner = COMMIT_REPORT_CONF['owner']
    repo_names = COMMIT_REPORT_CONF['repo_names']

    start_date = COMMIT_REPORT_CONF['start_date']
    if start_date:
        start_date = str(start_date)

    return owner, repo_names, start_date


def commits_to_csv(owner, repo_names, start_date=None):
    filename = CSV_OUT_NAME.format(
        end_date=datetime.date.today(),
        start_date=start_date if start_date else "INIT",
    )
    path = lib.VAR_DIR / filename
    for repo_name in repo_names:
        commits = repo_commits.get_commits(owner, repo_name, start_date)
        lib.write_csv(path, commits, append=True)


def main():
    """
    Main command-line function.
    """
    parser = argparse.ArgumentParser(description="Repo commits report")

    parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help="If supplied, list configured repos and date range",
    )

    args = parser.parse_args()

    owner, repo_names, start_date = report_config()

    if args.dry_run:
        print(lib.text.prettify((owner, repo_names, start_date)))
    else:
        commits_to_csv(
            owner,
            repo_names,
            start_date
        )


if __name__ == '__main__':
    main()
