"""
Report for recent commits of repos.
"""
import sys

import lib
import lib.text


# TODO Since param
# TODO: Refactor - move this function to lib.
def parse_commit(value):
    """
    Extract fields from nested data as returned from API and return as flat dict.
    """
    author = value["committer"]["user"]
    author_login = author["login"] if author is not None else None
    author_date = lib.time.as_date(value["authoredDate"])

    committer = value["committer"]["user"]
    committer_login = committer["login"] if committer is not None else None
    commit_date = lib.time.as_date(value["committedDate"])

    return dict(
        commit_id=value["abbreviatedOid"],
        author_date=author_date,
        author_login=author_login,
        committed_date=commit_date,
        committer_login=committer_login,
        changed_files=value["changedFiles"],
        additions=value["additions"],
        deletions=value["deletions"],
        message=value["message"],
    )


def main(args):
    """
    Main command-line function.
    """
    if len(args) not in (2, 4) or set(args).intersection({"-h", "--help"}):
        lib.text.eprint(f"Usage: {__file__} login LOGIN")
        sys.exit(1)

    path = "queries/repos/repos_recent_commits.gql"
    variables = lib.process_variables(args)

    out_data = []
    query_counter = 0

    while True:
        query_counter += 1
        print(f"Query #{query_counter}")
        data = lib.query_by_filename(path, variables)

        repositories = data["repositoryOwner"]["repositories"]
        if query_counter == 1:
            print(f"Total count: {repositories['totalCount']}")

        for repo_node in repositories["nodes"]:
            name = repo_node["name"]

            print(f"Name: {name}")

            branch = repo_node["defaultBranch"]
            if branch is not None:
                branch_name = branch["name"]

                commits = branch["commits"]["history"]["nodes"]

                for c in commits:
                    parsed_commit_data = parse_commit(c)
                    out_commit = dict(
                        repo_name=name,
                        branch_name=branch_name,
                        **parsed_commit_data,
                    )
                    out_data.append(out_commit)

        repo_page_info = repositories["pageInfo"]
        if repo_page_info["hasNextPage"]:
            variables["cursor"] = repo_page_info["endCursor"]
        else:
            break

    lib.write_csv(lib.VAR_DIR / "repos_recent_commits.txt", out_data)


if __name__ == "__main__":
    main(sys.argv[1:])
