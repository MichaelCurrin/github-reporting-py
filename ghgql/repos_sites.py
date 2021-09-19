#!/usr/bin/env python
"""
Repos sites application.

Get the URLs for repos.
"""
import json
import sys
from pathlib import Path

import lib.text

QUERY_PATH = Path("queries/repos/repos_sites.gql")
OUT_PATH = Path("var/sites.json")

dict_of_str = dict[str, str]
list_of_str = list[str]


def write_json(path: Path, rows: list[dict_of_str]):
    if not rows:
        print("No rows to write")
        print()
        return

    with open(path, "w") as f_out:
        json.dump(rows, f_out, indent=4)

    print("Wrote JSON:")
    print(f" - {path}")
    print(f" - {len(rows)} rows")
    print()


def get(path: Path, variables: dict_of_str):
    """
    Note that homepage URL may be null or an empty string in the API response.
    """
    repos = []

    query_counter = 0

    while True:
        query_counter += 1
        data = lib.query_by_filename(path, variables)

        repositories = data["repositoryOwner"]["repositories"]
        if query_counter == 1:
            print(f"Total count: {repositories['totalCount']}")

        for node in repositories["nodes"]:
            homepage_url = node["homepageUrl"]

            if not homepage_url:
                continue

            name = node["name"]
            repos.append({"name": name, "homepage_url": homepage_url})

        repo_page_info = repositories["pageInfo"]
        if repo_page_info["hasNextPage"]:
            variables["cursor"] = repo_page_info["endCursor"]
        else:
            break

    return repos


def process(path: Path, variables: dict_of_str, out_path: Path):
    """
    Fetch repo data and write results.
    """
    repos = get(path, variables)

    write_json(out_path, repos)


def main(args: list_of_str):
    """
    Main command-line function.
    """
    if len(args) != 2 or set(args).intersection({"-h", "--help"}):
        lib.text.eprint(f"Usage: {__file__} owner OWNER")
        sys.exit(1)

    variables = lib.process_variables(args)
    process(QUERY_PATH, variables, OUT_PATH)


if __name__ == "__main__":
    main(sys.argv[1:])
