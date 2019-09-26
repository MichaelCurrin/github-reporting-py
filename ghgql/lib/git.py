"""
Git library module.
"""
from . import time


def parse_commit(value):
    """
    Extract fields from nested data as returned from API and return as flat dict.
    """
    author = value['committer']['user']
    author_login = author['login'] if author is not None else None
    author_date = time.as_date(value['authoredDate'])

    committer = value['committer']['user']
    committer_login = committer['login'] if committer is not None else None
    commit_date = time.as_date(value['committedDate'])

    return dict(
        commit_id=value['abbreviatedOid'],
        author_date=author_date,
        author_login=author_login,

        committed_date=commit_date,
        committer_login=committer_login,

        changed_files=value['changedFiles'],
        additions=value['additions'],
        deletions=value['deletions'],
        message=value['message'],
    )


def prepare_row(commit, repo_name, branch_name):
    parsed_commit_data = parse_commit(commit)

    return dict(
        repo_name=repo_name,
        branch_name=branch_name,
        **parsed_commit_data,
    )
