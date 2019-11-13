"""
Query application.

Generic script to do a query against Github API using a given query's filepath.
The result will be pretty printed. Note that even if the query handles paging,
this script will only get the first page.
"""
import sys

import lib.text


def main(args):
    """
    Main command-line function.
    """
    if not args or set(args).intersection({'-h', '--help'}):
        lib.text.eprint(f"Usage: {__file__} QUERY_PATH [KEY VALUE[,KEY VALUE,...]]")
        lib.text.eprint("QUERY_PATH: Path to file containing query e.g. queries/commits.gql")
        lib.text.eprint(
            "For parametized/dynamic queries, provide an optional list of\n"
            "key-value pairs, separated by a space.\n"
            ' e.g. to send {"owner": "abc", "repo": "xyz 1"} in the variables, use\n'
            "   QUERY_PATH owner abc repo 'xyz 1'"
        )
        sys.exit(1)

    path, variables = lib.process_args(args)

    data = lib.query_by_filename(path, variables=variables)
    print(lib.text.prettify(data))


if __name__ == '__main__':
    main(sys.argv[1:])
