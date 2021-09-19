"""
Library text module.
"""
import json
import sys
from typing import Union


# TODO: Also write to log to make it easier to keep track of later.
def eprint(*args, **kwargs):
    """
    Print text to stderr.
    """
    print(*args, file=sys.stderr, **kwargs)


def prettify(data: Union[list, dict]):
    """
    Return input data structure (list or dict) as a prettified JSON-formatted string.

    Default is set here to stringify values like datetime values.
    """
    return json.dumps(data, indent=4, sort_keys=True, default=str)


def print_args_on_error(func):
    """
    Decorator used to print variables given to a function if the function
    call fails.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print("ARGS")
            print(*args)
            print("KWARGS")
            print(**kwargs)
            raise

    return wrapper


def parse_bool(value):
    value = value.lower()
    if value == "true":
        return True
    if value == "false":
        return False

    raise ValueError(f"Could not parse value to bool. Got: {value}")


def test():
    assert parse_bool("true") is True
    assert parse_bool("FALSE") is False
    assert parse_bool(None) is None
