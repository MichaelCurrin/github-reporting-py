"""
Basic application.

This is intended for newcomers to Python and/or GraphQL to see in one place
what the minimum components are to do a request and print the response.
This is just meant as a demo though, as it is too simple to be resuable or
robust.
"""
import json

import requests

import config


json_query = {
    'query': """
        query BasicQueryTest{
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

headers = {'Authorization': f"token {config.ACCESS_TOKEN}"}
resp = requests.post(config.BASE_URL, json=json_query, headers=headers)
prettified = json.dumps(resp.json(), indent=4)
print(prettified)
