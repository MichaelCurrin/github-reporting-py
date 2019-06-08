"""
Parametized demo application.

This is intended for newcomers to Python and/or GraphQL to see in one place
what the minimum components are to do a request and print the response.
This is just meant as a demo though, as it is too simple to be resuable or
robust.

This demo makes use of variables which are sent in the JSON payload. In
the GQL explorer, the variables would go in the Query Variables pane.

Query variables
    https://stackoverflow.com/questions/48693825/making-a-graphql-mutation-from-my-python-code-getting-error

    According to that SO post, query variables must be sent in on the JSON
    payload with the 'variables' key.
    request.post(..., json={'query': query, 'variables': variables}, ...)
"""
import json

import requests

import config


# Simple query with parametized repo owner and name values, to fetch the last
# 3 commits on the default branch.
json_query = {
    'query': """
        query BasicQueryTest($owner: String!) {
            repository(owner: $owner, name: "aggre-git") {
                defaultBranchRef {
                    target {
                        ... on Commit {
                            history(first: 3) {
                                edges {
                                    node {
                                        abbreviatedOid
                                        committedDate
                                        pushedDate
                                        message
                                        additions
                                        changedFiles
                                        deletions
                                        committer {
                                            user {
                                                login
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    """,
    'variables': {'owner': 'michaelcurrin'}
}

headers = {'Authorization': f"token {config.ACCESS_TOKEN}"}
resp = requests.post(config.BASE_URL, headers=headers, json=json_query,
                     )
prettified = json.dumps(resp.json(), indent=4)
print(prettified)
