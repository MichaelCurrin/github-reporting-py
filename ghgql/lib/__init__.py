"""
Library module.
"""
import csv
import datetime
import json
import sys
from pathlib import Path
from time import sleep

import config
import requests
from jinja2 import Template  # type: ignore

# TODO: Rename time to not conflict with builtin.
from . import text, time

# FIXME: this only happens to work in lib so should be more robust
APP_DIR = Path().absolute()
VAR_DIR = APP_DIR / "var"

COUNTS_CSV_PATH = VAR_DIR / "counts.csv"
# TODO: Add start date.
COUNTS_CSV_PATH_TODAY = VAR_DIR / f"counts-end-{datetime.date.today()}.csv"
STARRED_CSV_PATH = VAR_DIR / "starred.csv"

ERROR_QUERY_PATH = VAR_DIR / "error_query.gql"
ERROR_PAYLOAD_PATH = VAR_DIR / "error_payload.gql"

HEADERS = {"Authorization": f"token {config.ACCESS_TOKEN}"}
MAX_ATTEMPTS = 3


def _request(url, payload, headers):
    resp = requests.post(url, json=payload, headers=headers)
    resp_json = resp.json()

    errors = resp_json.get("errors", None)

    # TODO: Abort immediately on bad syntax or bad/missing variable.
    if errors:
        error_msg = errors.get("message", None)
        if error_msg == "Bad credentials":
            print("Update the configured token and try again")
            sys.exit(1)

        print(f"Writing query to: {ERROR_QUERY_PATH}")
        write_file(payload["query"], ERROR_QUERY_PATH)

        print(f"Writing payload to: {ERROR_PAYLOAD_PATH}")
        write_file(payload, ERROR_PAYLOAD_PATH)

        msg = text.prettify(errors)

        raise ValueError(f"Error requesting GitHub. Errors:\n{msg}")

    if (resp_json.get("data", None)) is None:
        message = text.prettify(resp_json)

        raise ValueError(f"Error requesting GitHub. Details:\n{message}")

    return resp_json


def fetch_github_data(query: str, variables=None) -> dict:
    """
    Get data from GitHub API using given parameters.

    Note that a request which returns an error will still give a 200 and can
    might still contain some data. A 404 will not contain the data or errors
    keys.
    """
    if not variables:
        variables = {}

    payload = {
        "query": query,
        "variables": variables,
    }

    resp_json = {}

    for i in range(MAX_ATTEMPTS):
        try:
            resp_json = _request(config.BASE_URL, payload, HEADERS)
        except ValueError as e:
            text.eprint(f"Requested failed - attempt #{i+1}/{MAX_ATTEMPTS}")

            if i + 1 == MAX_ATTEMPTS:
                raise
            text.eprint(e)

            if "rate" in str(e):
                print("RATE LIMITED")

            # TODO: Sleep for set time or perhaps short time if too frequent
            # between requests.
            seconds = 10
            text.eprint(f"Sleeping {seconds} s...")
            sleep(seconds * 1000)
            text.eprint("Retrying...")
        else:
            break

    return resp_json.get("data", None)


def read_file(path):
    """
    TODO: Refactor to use Path().read() instead.
    """
    with open(path) as f_in:
        file_text = f_in.read()

    return file_text


def write_file(content, path):
    """
    Write a list or str to a given filepath.

    TODO: Refactor to use Path() with appropriate text or JSON method.
    """
    if isinstance(content, (list, dict)):
        content = json.dumps(content)

    print("Writing")
    print(f" - path: {path}")

    with open(path, "w") as f_out:
        f_out.writelines(content)


def read_template(path: Path):
    """
    Return Jinja template at a given path.
    """
    return Template(read_file(path))


# TODO Rename to path.
# TODO Refactor so the file only has to be read once for a set of paged queries.
def query_by_filename(path, variables=None):
    if not variables:
        variables = {}
    query = read_file(path)
    resp = fetch_github_data(query, variables)

    return resp


def read_csv(path: Path):
    with open(path) as f_in:
        reader = csv.DictReader(f_in)

        return list(reader)


def write_csv(path: Path, rows: list[dict], append=False) -> None:
    """
    Write a CSV file to a path with given rows and header from first row.

    Default behavior is to overrwrite an existing file. Append to existing file
    if append is flag True. Either way, the header will only be added on a new
    file. Appending is useful when adding sections to a report, but overwriting
    is better when rerunning an entire report.
    """
    if not rows:
        print("No rows to write")
        print()

        return

    is_new_file = not path.exists()
    mode = "a" if append else "w"

    fieldnames = list(rows[0].keys())

    with open(path, mode) as f_out:
        writer = csv.DictWriter(f_out, fieldnames)

        if is_new_file or not append:
            writer.writeheader()
        writer.writerows(rows)

    # TODO: How to include `var/name` if relevant. To make it easy to click on console output.
    print("Wrote CSV:")
    print(f" - {path.name}")
    print(f" - {len(rows)} rows {'appended' if append else ''}")
    print()


def process_variables(args: list[str]) -> dict:
    """
    Process command-line arguments containing a filename and key-value pairs.
    """
    if args:
        if len(args) % 2:
            raise ValueError(f'Incomplete key-value pairs provided: {" ".join(args)}')
        variables = dict(zip(args[::2], args[1::2]))

        # TODO: Make this clear that you use start and it becomes since.
        start = variables.pop("start", None)
        if start:
            variables["since"] = time.as_git_timestamp(start)

        is_fork_arg = variables.pop("isFork", None)
        if is_fork_arg:
            variables["isFork"] = text.parse_bool(is_fork_arg)

        return variables

    return {}


def process_args(args: list[str]):
    """
    Process command-line arguments containing a filename and key-value pairs.

    Separate args into filepath and optional key-value pairs, with spaces
    between pairs and within pairs. Rather than setting allowed keys, any
    key is allowed.
    """
    path = args.pop(0)
    variables = process_variables(args)

    return path, variables


def to_archive_url(owner: str, repo_name: str, branch: str) -> str:
    """
    Return a download URL for a repo's zip file.
    """
    return f"https://github.com/{owner}/{repo_name}/archive/{branch}.zip"
