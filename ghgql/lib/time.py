"""
Library time module.
"""
import datetime


def timestamp(date_str):
    """
    Convert string matching "YYYY-MM-DD" into GitTimestamp string.
    """
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').isoformat()


def as_date(datetime_str: str) -> datetime.date:
    """
    Convert string which starts with "YYYY-MM-DD" to a date object.
    """
    date_str = datetime_str[:10]

    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
