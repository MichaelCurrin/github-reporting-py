# Github GraphQL Tool
> Python tool to easily report on data fetched from Github's GraphQL API

Github's v4 API is no longer REST but GraphQL and this project explores that for reporting purposes. Such as creating text or CSV reports for given parameters, so you can understand the git history of one or more repos and how you or your team contribute to the repos.


## Example output

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
                            ...
```


## GraphQL benefits

The GraphQL single endpoint allows fetching of large amounts of data with fewer queries than REST, getting just the fields and level of detail requested. Note that paging and rate limits still apply but should be easier to deal with.

In particular, GraphQL makes easier to scale to many fetch a large numbers of commits, even across multiple repos or branches, using a single request. Whereas the REST API only gives the commit data at the branch tip. So to get a 1000 commits you need 1000 requests. This is slow and results in quick rate limiting (max 5000 requests per hour). I experience this in a previous project.


## Requirements

- Github account
- Github API token with access to repos
- Python 3


## Documentation

See the following guides for this project. Note that documentation only covers installing and running on a Unix-style environment.

- [Installation](/docs/installation.md)
- [Usage](/docs/Usage.md)
