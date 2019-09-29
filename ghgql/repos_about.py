#!/usr/bin/env python
"""
About repos application.

Print results for the about repos query for a given login.
"""
import sys

import lib.text


def main(args):
    """
    Main command-line function.
    """
    if len(args) != 2 or set(args).intersection({'-h', '--help'}):
        lib.text.eprint(f"Usage: {__file__} login LOGIN")
        sys.exit(1)

    path = 'queries/repos/repos_about.gql'
    variables = lib.process_variables(args)

    query_counter = 0
    while True:
        query_counter += 1
        print(f"Query #{query_counter}")
        data = lib.query_by_filename(path, variables)

        repositories = data['repositoryOwner']['repositories']
        if query_counter == 1:
            print(f"Total count: {repositories['totalCount']}")

        for node in repositories['nodes']:
            name = node['name']
            description = node['description'] or "N/A"
            created_at = node['createdAt'][:10]
            updated_at = node['updatedAt'][:10]
            primary_lang = (node['primaryLanguage'] or {}).get('name', "N/A")
            langs = [x['name'] for x in node['languages']['nodes']]
            langs_txt = ", ".join(langs) if langs else "N/A"
            print(f"Name: {name}")
            print(f"Description: {description}")
            print(f"Updated: {updated_at}")
            print(f"Created: {created_at}")
            print(f"Primary language: {primary_lang}")
            print(f"Languages: {langs_txt}")
            print()

        repo_page_info = repositories['pageInfo']
        if repo_page_info['hasNextPage']:
            variables['cursor'] = repo_page_info['endCursor']
        else:
            break


if __name__ == '__main__':
    main(sys.argv[1:])
