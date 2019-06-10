"""
Query application.

Dynamically select a query using a filepath, send as a request to Github
and pretty print the results.
"""
import sys

import requests

import config
import lib


def main(args):
    if not args or set(args).intersection({'-h', '--help'}):
        print(f"Usage: {__file__} QUERY_PATH [KEY VALUE[,KEY VALUE,...]]")
        print("QUERY_PATH: Path to file containing query e.g. queries/commits.gql")
        print("For parametized/dynamic queries, provide an optional list of"
              " key-value pairs, separated by a space."
              ' e.g. to send {owner: "michaelcurrin"} in the variables, use\n'
              "   owner michaelcurrin"
              )
        sys.exit(1)

    path = args.pop(0)
    if args:
        if len(args) % 2:
            raise ValueError(f'Incomplete key-value pairs provided: {" ".join(args)}')
        variables = dict(zip(args[::2], args[1::2]))
    else:
        variables = None

    data = lib.query_by_filename(path, variables=variables)
    print(lib.prettify(data))


if __name__ == '__main__':
    main(sys.argv[1:])
