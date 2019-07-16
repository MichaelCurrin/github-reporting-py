"""
Pagination demo application.

Simple demo to show multiple queries done automatically using returned
cursor value to fetch the next page. The number of pages is capped
to make this a quick script.

No arguments are used for this script.
"""
import lib


def main():
    """
    Main command-line function.

    Do a query to the API using a configured GQL file and query variables.
    In this situation, the only variable to send is 'cursor'.
    """
    path = 'queries/paged/commits_basic.gql'
    variables = {}
    for i in range(5):
        print(f"Query #{i+1} - cursor: {variables.get('cursor', 'null')}")

        data = lib.query_by_filename(path, variables=variables)
        history = data['repository']['defaultBranchRef']['target']['history']

        msgs = [edge['node']['message'] for edge in history['edges']]
        for msg in msgs:
            print(f"  {msg}")

        page_info = history['pageInfo']
        has_next_page = page_info['hasNextPage']
        if not has_next_page:
            print("No more pages")
            break
        variables['cursor'] = page_info['endCursor']


if __name__ == '__main__':
    main()
