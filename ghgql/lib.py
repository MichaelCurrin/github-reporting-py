import json
import os

import requests

import config

HEADERS = {'Authorization': f"token {config.ACCESS_TOKEN}"}


def prettify(data):
    return json.dumps(data, indent=4, sort_keys=True)


def fetch_github_data(query, prettyprint=False):
    """
    Note that a request which returns an error will still give a 200.
    The data key is expected, but there could be an errors key for 404
    there can be others.
    """
    resp = requests.post(
        config.BASE_URL,
        json={'query': query},
        headers=HEADERS
    ).json()

    data = resp.get('data', None)

    if data is None:
        message = prettify(resp)
        raise ValueError(f"Error requesting Github GQL endpoint:\n{message}")

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
