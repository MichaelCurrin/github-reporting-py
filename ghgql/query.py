#!/usr/bin/env python
"""
Query application.

Generic script to do a query against Github API using a given query's filepath
and optionally send a data payload using key-value pairs provided. The result
will be pretty printed as JSON, without any processing.

Note that even if the query handles paging, this script will only get the first
page.
"""
import sys

import lib.text


def main(args):
    """
    Main command-line function.
    """
    # TODO: Refactor strings here to be easy to edit and not exceed char limit.
    if not args or set(args).intersection({'-h', '--help'}):
        script_path = f"./{__file__}" if not __file__.startswith(
            './') else __file__
        lib.text.eprint(
            f"Usage: {script_path} QUERY_PATH [KEY VALUE[,KEY VALUE,...]]\n"
            "\nDo a query to the Github GraphQL API using path to query,"
            " plus optional variables\n"
        )

        lib.text.eprint(
            "QUERY_PATH: Path to file containing query. This can be anywhere but is typically\n"
            "            from the project's query directory. e.g. queries/user/user_me.gql\n"
        )
        lib.text.eprint(
            "KEY VALUE:  For parametized/dynamic queries, provide an optional list of\n"
            "            key-value pairs, with spaces between pairs and within pairs.\n\n"
            '            To send {"owner": "abc", "repo": "xyz 1"} in the variables,\n'
            "            provide variables as\n"
            "               owner abc repo 'xyz 1'"
        )
        lib.text.eprint(
            "\nSince the API allows a max of 100 items on page, the script will"
            '\npaginate through the pages of results. The "after" indicator for '
            "\nthe next page is added internally to the variables sent in the"
            "\npayload, so paging will happen automatically."
            "\n"
        )
        sys.exit(1)

    path, variables = lib.process_args(args)

    data = lib.query_by_filename(path, variables=variables)
    print(lib.text.prettify(data))


if __name__ == '__main__':
    main(sys.argv[1:])
