#!/usr/bin/env python
"""
Starred repos report application.

Get metadata for which the current user has starred and then write to a CSV.
"""
import sys

import lib
import lib.text


def parse_repo(node):
    """
    Get revelant fields from a given repo.
    
    :param node dict: A repo fetched from the GQL API.
    
    :return: A dict of processed details for the given repo.
    """
    owner = node["owner"]["login"]
    repo_name = node["name"]

    latest_releases = node["latestRelease"]["nodes"]

    if node["branch"]:
        branch = node["branch"]["name"]
        archive_url = lib.to_archive_url(owner, repo_name, branch)
    else:
        branch = archive_url = None

    return dict(
        owner=owner,
        name=repo_name,
        description=node["description"] or "N/A",
        home_page_url=node["homepageUrl"],
        created_at=node["createdAt"][:10],
        updated_at=node["updatedAt"][:10],
        latest_release=latest_releases[0] if latest_releases else None,
        branch=branch,
        url=node["url"],
        ssh_url=node["sshUrl"],
        fork_count=node["forkCount"],
        archive_url=archive_url,
    )


def main(args):
    """
    Main command-line function.
    """
    if set(args).intersection({"-h", "--help"}):
        lib.text.eprint(f"Usage: {__file__} [cursor CURSOR]")
        sys.exit(1)

    path = "queries/repos/starred.gql"
    variables = lib.process_variables(args)

    results = []

    query_counter = 0
    while True:
        query_counter += 1
        print(f"Query #{query_counter}")
        
        data = lib.query_by_filename(path, variables)
        repositories = data["viewer"]["starredRepositories"]
        
        if query_counter == 1:
            print(f"Total count: {repositories['totalCount']}")
        for node in repositories["nodes"]:
            results.append(parse_repo(node))

        repo_page_info = repositories["pageInfo"]
        if repo_page_info["hasNextPage"]:
            variables["cursor"] = repo_page_info["endCursor"]
        else:
            break

    lib.write_csv(lib.STARRED_CSV_PATH, results)


if __name__ == "__main__":
    main(sys.argv[1:])
