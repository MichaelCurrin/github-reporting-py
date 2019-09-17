"""
Library module.
"""
import csv
from pathlib import Path

import requests
from jinja2 import Template

import config
from . import text, time


APP_DIR = Path().absolute()
VAR_DIR = APP_DIR / 'var'
COUNTS_CSV_PATH = VAR_DIR / 'counts.csv'

HEADERS = {'Authorization': f"token {config.ACCESS_TOKEN}"}


def fetch_github_data(query, variables=None):
    """
    Note that a request which returns an error will still give a 200 and can
    still contain some data. A 404 will not contain the data or errors keys.
    """
    if not variables:
        variables = {}

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
        message = text.prettify(errors)
        raise ValueError(f"Error requesting Github. Errors:\n{message}")

    data = resp.get('data', None)
    if data is None:
        message = text.prettify(resp)
        raise ValueError(f"Error requesting Github. Details:\n{message}")

    return data


def read_file(path):
    with open(path) as f_in:
        file_text = f_in.read()

    return file_text


def read_template(path):
    return Template(read_file(path))


# TODO Rename to path.
# TODO Refactor so the file only has to be read once for a set of paged queries.
def query_by_filename(path, variables=None):
    if not variables:
        variables = {}
    query = read_file(path)
    resp = fetch_github_data(query, variables)

    return resp


def read_csv(path):
    with open(path) as f_in:
        reader = csv.DictReader(f_in)

        return list(reader)


def write_csv(path, rows):
    fieldnames = rows[0].keys()
    with open(path, 'w') as f_out:
        writer = csv.DictWriter(f_out, fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Wrote CSV:")
    print(f" - {path}")
    print(f" - {len(rows)} rows")


def process_variables(args):
    """
    Process command-line arguments containing a filename and key-value pairs.
    """
    if args:
        if len(args) % 2:
            raise ValueError(f'Incomplete key-value pairs provided: {" ".join(args)}')
        variables = dict(zip(args[::2], args[1::2]))

        start = variables.pop('start', None)
        if start:
            variables['since'] = time.timestamp(start)

        is_fork_arg = variables.pop('isFork', None)
        if is_fork_arg:
            variables['isFork'] = text.parse_bool(is_fork_arg)

        return variables

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
