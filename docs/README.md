# GitHub Reporting Tool docs
> Create detailed and summary CSV reports of activity by a GitHub user, using the GraphQL API

[![Made with Python](https://img.shields.io/badge/Python->=3.9-blue?logo=python&logoColor=white)](https://python.org)
[![API - GitHub GraphQL](https://img.shields.io/badge/GitHub_API-V4_GraphQL-blue?logo=github)](https://graphql.github.io/)

A project to output CSV reports around on repos, users and commits, for interest and for business reporting.

View the source:

[![MichaelCurrin - github-reporting-py](https://img.shields.io/static/v1?label=MichaelCurrin&message=github-reporting-py&color=blue&logo=github)](https://github.com/MichaelCurrin/github-reporting-py)

If you're interested in making your own docs site like this one, follow my [DocsifyJS Tutorial](https://michaelcurrin.github.io/docsify-js-tutorial/).


## Sample

This project has a few executable Python scripts which each generate a report.

Run the script by name and supply it with arguments.

Examples:

```bash
$ ./repos_and_commit_counts.py owner MichaelCurrin
```

```
$ ./repos_and_commit_counts.py owner MichaelCurrin start 2020-04-01
```


## Documentation

See the following guides so you can use this project to generate some reports for yourself on users or repos you are interested in. Note that these only cover the case of a Unix-style environment.

- [Aims](/aims.md) - The main purposes for this project and how they could benefit you.
- [Installation](/installation.md) - Requirements and how to set up your environment and configs.
- [Usage](/usage.md) - Run CLI scripts to generate reports.
- [Datasources](/datasources.md) - Info and links around APIs.

See also GitHub's resources and samples for running GraphQL queries - [platform-samples](https://github.com/github/platform-samples/tree/master/graphql).
