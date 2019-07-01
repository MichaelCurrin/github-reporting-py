"""
Library module.
"""
import json
import os
import sys

import requests

import config

HEADERS = {'Authorization': f"token {config.ACCESS_TOKEN}"}


def eprint(*args, **kwargs):
    """
    Print text to stderr.
    """
    print(*args, file=sys.stderr, **kwargs)


def prettify(data):
    """
    Return input data structure (list or dict) as a prettified JSON string.
    """
    return json.dumps(data, indent=4, sort_keys=True)


def fetch_github_data(query, variables={}):
    """
    Note that a request which returns an error will still give a 200 and can
    still contain some data. A 404 will not contain the data or errors keys.
    """
    payload = {
        'query': query,
        'variables': variables,
    }
    resp = requests.post(
        config.BASE_URL,
        json=payload,
        headers=HEADERS
    ).json()

    errors = resp.get('errors', None)
    if errors:
        message = prettify(errors)
        raise ValueError(f"Error requesting Github. Errors:\n{message}")

    data = resp.get('data', None)
    if data is None:
        message = prettify(resp)
        raise ValueError(f"Error requesting Github. Details:\n{message}")

    return data


def read_file(path):
    assert os.access(path, os.R_OK), f"Cannot find file: {path}"
    with open(path) as f_in:
        data = f_in.read()

    return data


# TODO Rename to path.
def query_by_filename(path, variables={}):
    query = read_file(path)
    resp = fetch_github_data(query, variables)

    return resp


def process_variables(args):
    """
    Process command-line arguments containing a filename and key-value pairs.
    """
    if args:
        if len(args) % 2:
            raise ValueError(f'Incomplete key-value pairs provided: {" ".join(args)}')
        return dict(zip(args[::2], args[1::2]))

    return None


def process_args(args):
    """
    Process command-line arguments containing a filename and key-value pairs.

    Separate args into filepath and optional key-value pairs, with spaces
    between pairs and within pairs. Rather than setting allowed keys, any
    key is allowed.
    """
    path = args.pop(0)
    variables = process_variables(args)

    return path, variables
