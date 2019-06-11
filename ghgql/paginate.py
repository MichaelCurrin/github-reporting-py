"""
Query with pagination application.
"""
import sys

import config
import lib


def main():
    path = 'queries/paged/commits.gql'
    variables = {}
    for i in range(5):
        print(f"Query #{i+1}")
        data = lib.query_by_filename(path, variables=variables)
        history = data['repository']['defaultBranchRef']['target']['history']

        messages = [edge['node']['message'] for edge in history['edges']]
        for m in messages:
            print(f"  {m}")

        page_info = history['pageInfo']
        has_next_page = page_info['hasNextPage']
        if not has_next_page:
            print("No more pages")
            break
        after = page_info['endCursor']
        variables['after'] = after
        print(f"Next page starts after: '{after}'")
        print()


if __name__ == '__main__':
    main()
