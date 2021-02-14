"""
Basic query demo application.

This is intended for newcomers to Python and/or GraphQL to see in one place
what the minimum components are to do a request and print the response.
This is just meant as a demo though, as it is too simple to be reusable or
robust.

See also the parametrized demo script in the same directory.
"""
import json

import requests

import config


# Simple query with hardcoded repo owner and name to fetch the last 3 commits
# on the default branch.
payload = {
    "query": """
        query BasicQueryTest {
            repository(owner: "michaelcurrin", name: "aggre-git") {
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
    """
}

# Request headers - GitHub auth token is needed.
headers = {"Authorization": f"token {config.ACCESS_TOKEN}"}

# Send the POST request.
resp = requests.post(config.BASE_URL, json=payload, headers=headers)

# Pretty print the output.
prettified = json.dumps(resp.json(), indent=4)
print(prettified)
