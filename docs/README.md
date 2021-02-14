# GitHub Reporting Tool docs
> Create detailed and summary CSV reports of GitHub activity in a target GH user or organization

[![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://python.org)
[![API - GitHub GraphQL](https://img.shields.io/badge/GitHub_API-V4_GraphQL-blue?logo=github)](https://graphql.github.io/)

A project to output CSV reports around on repos, users and commits, for interest and for business reporting. Built on Python3 and GH GraphQL V4 API.


## Requirements

You need the following to run this project:

| Name                                                   | Description                               |
| ------------------------------------------------------ | ----------------------------------------- |
| GitHub account                                         | Needed to create a dev token.             |
| [GitHub dev token](https://github.com/settings/tokens) | For authenticated API requests.           |
| [Python](python.org/)                                  | Used to run queries and generate reports. |

Only **read** access to public repos is needed. You may also enable read access to any **private** repos which you have access to - either directly in your user or in an org that your user belongs to.


## Documentation

See the following guides so you can use this project to generate some reports for yourself on users or repos you are interested in. Note that these only cover the case of a Unix-style environment.

- [Aims](/aims.md) - The main purposes for this project and how they could benefit you.
- [Installation](/installation.md) - Setup project environment and configs.
- [Usage](/usage.md) - Run scripts to generate reports.
- [Datasources](/datasources.md) - Info and links around APIs.

See also GitHub's resources and samples for running GraphQL queries - [platform-samples](https://github.com/github/platform-samples/tree/master/graphql).
