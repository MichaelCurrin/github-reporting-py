# Github GraphQL Tool
> Python tool to easily report on data fetched from Github's GraphQL API

## Aim

The aim of this project is to fetch stats about Github repos of interest and to generate text or CSV reports, using input parameters. The GraphQL API is used to get this data at scale, to make reporting on a large Gitub organization easy.

This project is still in development. But the kind of reporting is to let you view the git commit history across multiple repos and to see how your organization or team members contribute (e.g. frequency and size of commits). The reports can also be aggregated such as with an Excel pivot table.

Don't use git reporting alone to judge your team's productivity or codebase, but reports can help you see patterns or blockers and that can help you identify problems to solve or areas to improve on.

Another aim of this project is to introduce coders to processing GraphQL queries using Python. The understanding can be applied to other GraphQL APIs.

## Datasource

[Github](https://github.com) hosts code for developers and organizations and makes the code and history available through an API. Version 3 used REST but version 4 uses GraphQL - this project explores using GraphQL API for reporting purposes, in particular because GraphQL is more modern and can scale easier for download data.

*What a [REST](https://www.restapitutorial.com/) API? What is [GraphQL](https://graphql.org/)?*

You can test queries against Github data in the [GraphQL explorer](https://developer.github.com/v4/explorer/). The interactive view there makes it easy to explorer the schema.

## Sample output

One of the scripts in this Github GraphQL Tool project will give the following output:

```bash
$ PYTHONPATH=$(pwd) python demo/basic.py
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


## GraphQL benefits

Using [GraphQL](https://graphql.org/) means only a single endpoint to query, using a POST request usually to get data. It allows fetching of large amounts of data with fewer queries than REST, getting just the fields and level of detail requested. Note that paging and rate limits still apply but should be easier to deal with.

In particular, **GraphQL** makes it easier to scale to many fetch a large numbers of commits, even across multiple repos or branches, using a single request.  Although, there is a strict API limit of a **max of 100 items** in a list, so you need to use multiple requests to paginate through the data. But in a single request, you can still fetch 100 repos and the most recent 100 commits on each.

This is still much better than the **REST API**, which only lets you query one repo at a time and only gives a single commit and a pointer to the previous commit (or _commits_, for a merge). This is slow and results in quick rate limiting (max 5000 requests per hour). I experienced this in a similar previous project which used a Python wrapper on the Github REST API.

GraphQL is 100 times faster at getting commits and 100 times faster at getting repos, resulting in a gain of 10,000 times faster performance. For example, given a scenario to get 1,000 commits for the default branches of 100 repos, here are the number of requests required:

- **REST API**: 100 repos x 1000 commits for each = *100,000 requests*
- **GraphQL API**: 1 page of repos x 10 commit pages = *10 requests*


## Requirements

You need the following to run this project:

- Github account
- Github API token with access to repos
- Internet connection
- Python 3


## Documentation

See the following guides so you can use this project to generate some reports for yourself on users or repos you are interested in. Note that these only cover the case of a Unix-style environment.

- [Installation](/docs/installation.md)
- [Usage](/docs/usage.md)
