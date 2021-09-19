"""
Query variables demo application.

This is intended for newcomers to Python and/or GraphQL to see in one place
what the minimum components are to do a request and print the response, using
variables. This is just meant as a demo though, as it is too simple to be
resuable or robust.

See also the basic demo script in the same directory.

This script makes use of variables which are sent in the JSON payload. The
variables are already setup so no arguments are needed for this script. In
the GQL explorer, the variables data would go in the Query Variables pane.

Query variables
    https://stackoverflow.com/questions/48693825/making-a-graphql-mutation-from-my-python-code-getting-error

    According to that SO post, query variables must be sent in on the JSON
    payload with the 'variables' key.
    request.post(..., json={'query': query, 'variables': variables}, ...)
"""
import json

import config
import requests

# Simple query with parametized repo owner and name values, to fetch the last
# 3 commits on the default branch.
payload = {
    "query": """
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
    "variables": {"owner": "michaelcurrin", "name": "aggre-git"},
}

# Request headers - GitHub auth token is needed.
headers = {"Authorization": f"token {config.ACCESS_TOKEN}"}

# Send the POST request.
resp = requests.post(config.BASE_URL, json=payload, headers=headers)

# Pretty print the output.
prettified = json.dumps(resp.json(), indent=4)
print(prettified)
