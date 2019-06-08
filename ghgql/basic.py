"""
Basic

Demo doing and printing a request response, with emphasis on readability.
"""
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
print(resp.json())
