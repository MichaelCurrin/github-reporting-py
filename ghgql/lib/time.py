"""
Library time module.
"""
import datetime


def as_git_timestamp(value: [datetime.date, datetime.datetime, str]) -> str:
    """
    Convert date to GitTimestamp string.

    The output format is the datetime formatted string required by Github's
    GraphQL. Any time in the input value is dropped so the result is for
    midnight.
    """
    dt = datetime.datetime.strptime(str(value), '%Y-%m-%d')

    return dt.isoformat()


def as_date(datetime_str: str) -> datetime.date:
    """
    Convert string which starts with "YYYY-MM-DD" to a date object.
    """
    date_str = datetime_str[:10]

    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


def days_ago(days: int) -> datetime.date:
    """
    Lookback a given number of days from today and return a date object.
    """
    return datetime.date.today() - datetime.timedelta(days=days) + datetime.timedelta(days=1)
