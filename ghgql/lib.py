"""
Library module.
"""
import json
import os

import requests

import config

HEADERS = {'Authorization': f"token {config.ACCESS_TOKEN}"}


def prettify(data):
    return json.dumps(data, indent=4, sort_keys=True)


def fetch_github_data(query, variables={}, prettyprint=False):
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


def query_by_filename(path):
    query = read_file(path)
    resp = fetch_github_data(query, prettyprint=True)

    return resp
