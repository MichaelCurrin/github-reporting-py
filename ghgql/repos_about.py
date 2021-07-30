#!/usr/bin/env python
"""
About repos report application.

Get the metadata for a repos of a given login and print.

TODO: Write to CSV.
"""
import sys

import lib.text

QUERY_PATH = "queries/repos/repos_about.gql"


def process(repo_node):
    name = repo_node["name"]
    description = repo_node["description"] or "N/A"

    created_at = repo_node["createdAt"][:10]
    updated_at = repo_node["updatedAt"][:10]

    primary_lang = (repo_node["primaryLanguage"] or {}).get("name", "N/A")
    langs = [x["name"] for x in repo_node["languages"]["nodes"]]
    langs_txt = ", ".join(langs) if langs else "N/A"

    print(f"Name: {name}")
    print(f"Description: {description}")
    print(f"Updated: {updated_at}")
    print(f"Created: {created_at}")
    print(f"Primary language: {primary_lang}")
    print(f"Languages: {langs_txt}")
    print()


def report(path, variables):
    query_counter = 0

    while True:
        query_counter += 1
        print(f"Query #{query_counter}")

        data = lib.query_by_filename(path, variables)
        repositories = data["repositoryOwner"]["repositories"]

        repo_nodes = repositories["nodes"]
        total = repositories["totalCount"]
        repo_page_info = repositories["pageInfo"]

        if query_counter == 1:
            print(f"Total count: {total}")

        for repo_node in repo_nodes:
            process(repo_node)

        if repo_page_info["hasNextPage"]:
            variables["cursor"] = repo_page_info["endCursor"]
        else:
            break


def main(args):
    """
    Main command-line function.
    """
    if len(args) != 2 or set(args).intersection({"-h", "--help"}):
        lib.text.eprint(f"Usage: {__file__} owner OWNER")
        sys.exit(1)

    path = QUERY_PATH
    variables = lib.process_variables(args)
    report(path, variables)


if __name__ == "__main__":
    main(sys.argv[1:])
