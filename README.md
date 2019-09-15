# Github GraphQL Tool
> Python tool to easily report on data fetched from Github's GraphQL API

## Aim

The aim of this project is to fetch stats about Github repos of interest and to generate text or CSV reports, using input parameters. The GraphQL API is used to get this data at scale, to make reporting on a large Github organization easy.

This project is still in development. But the kind of reporting is to let you view the git commit history across multiple repos and to see how your organization or team members contribute (e.g. frequency and size of commits). The reports can also be aggregated such as with an Excel pivot table.

Don't use git reporting alone to judge your team's productivity or codebase, but reports can help you see patterns or blockers and that can help you identify problems to solve or areas to improve on.

Another aim of this project is to introduce coders to processing GraphQL queries using Python. The understanding can be applied to other GraphQL APIs.

## Example output

Output from a very basic demo script. It queries the Github GraphQL API with fixed parameters, parses the JSON data in the response printed and prints it.

```bash
$ python -m python demo.basic
```
```
{
    "data": {
        "repository": {
            "defaultBranchRef": {
                "target": {
                    "history": {
                        "edges": [
                            {
                                "node": {
                                    "abbreviatedOid": "5c8a856",
                                    "committedDate": "2019-01-21T14:19:46Z",
                                    "pushedDate": "2019-01-21T14:19:49Z",
                                    "message": "docs: Update comments and docstring around Jira tickets",
                                    "additions": 6,
                                    "changedFiles": 1,
                                    "deletions": 4,
                                    "committer": {
                                        "user": {
                                            "login": "MichaelCurrin"
                                        }
                                    }
                                }
                            },
                            ...,
                            ...,
                        ]
                    }
                }
            }
        }
    }
}
```


## Project Requirements

You need the following to run this project:

- Github account
- Github API token with access to repos
- Internet connection
- Python 3.6+


## Documentation

See the following guides so you can use this project to generate some reports for yourself on users or repos you are interested in. Note that these only cover the case of a Unix-style environment.

- [Datasources](/docs/datasources.md)
- [Installation](/docs/installation.md)
- [Usage](/docs/usage.md)
