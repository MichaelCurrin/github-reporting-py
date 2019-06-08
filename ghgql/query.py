"""
Query.

Dynamically select a query using a filepath, send as a request to Github
and pretty print the results.
"""
import sys

import requests

import config
import lib


def main(args):
    if not len(args) == 1 or set(args).intersection({'-h', '--help'}):
        print(f"Usage: {__file__} QUERY_PATH")
        print("QUERY_PATH: Path to file containing query e.g. queries/commits.gql")
        sys.exit(1)

    path = args.pop(0)
    data = lib.query_by_filename(path)
    print(lib.prettify(data))


if __name__ == '__main__':
    main(sys.argv[1:])
