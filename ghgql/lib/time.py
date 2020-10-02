"""
Library time module.
"""
import datetime
from typing import Union


def as_git_timestamp(value: Union[datetime.date, datetime.datetime, str]) -> str:
    """
    Convert date to ISO timestamp string.

    Output as an ISO datetime format string, as required by the GitHub
    GraphQL schema's `GitTimestamp` object.

    Any time in the input value gets dropped, such that the time is at midnight.
    """
    dt = datetime.datetime.strptime(str(value), "%Y-%m-%d")

    return dt.isoformat()


def as_date(dt: str) -> datetime.date:
    """
    Convert string which starts with "YYYY-MM-DD" to a date object.
    """
    date = dt[:10]

    return datetime.datetime.strptime(date, "%Y-%m-%d").date()


def days_ago(days: int) -> datetime.date:
    """
    Lookback a given number of days from today and return a date object.
    """
    return (
        datetime.date.today()
        - datetime.timedelta(days=days)
        + datetime.timedelta(days=1)
    )
