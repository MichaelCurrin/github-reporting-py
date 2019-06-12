"""
Pagination demo application.
"""
import sys

import config
import lib


def main():
    path = 'queries/paged/commits_basic.gql'
    variables = {}
    for i in range(5):
        after = variables.get('after', None) or "null"
        print(f"Query #{i+1} - after: {after}")

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
        variables['after'] = page_info['endCursor']


if __name__ == '__main__':
    main()
