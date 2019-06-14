"""
Query application.

Dynamically select a query using a filepath, send as a request to Github
and pretty print the results.
"""
import sys

import config
import lib


def main(args):
    if not args or set(args).intersection({'-h', '--help'}):
        print(f"Usage: {__file__} QUERY_PATH [KEY VALUE[,KEY VALUE,...]]")
        print("QUERY_PATH: Path to file containing query e.g. queries/commits.gql")
        print("For parametized/dynamic queries, provide an optional list of\n"
              "key-value pairs, separated by a space.\n"
              ' e.g. to send {"owner": "michaelcurrin"} in the variables, use\n'
              "   QUERY_PATH owner michaelcurrin"
              )
        sys.exit(1)

    path, variables = lib.process_args(args)

    data = lib.query_by_filename(path, variables=variables)
    print(lib.prettify(data))


if __name__ == '__main__':
    main(sys.argv[1:])
