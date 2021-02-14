# GitHub Reporting Tool
> Create detailed and summary CSV reports of GitHub activity in a target GH user or organization

A project to output CSV reports around on repos, users and commits, for interest and for business reporting. Built on Python3 and GH GraphQL V4 API.


## Requirements

You need the following to run this project:

| Name                                                   | Description                               |
| ------------------------------------------------------ | ----------------------------------------- |
| GitHub account                                         | Needed to create a dev token.             |
| [GitHub dev token](https://github.com/settings/tokens) | For V4 GraphQL API requests.              |
| [Python](python.org/) >= 3.6                           | Used to run queries and generate reports. |

Only read access to repos is needed. You may enable read access to private repos which you have access to through being a member of an GitHub org (such as your work).


## Documentation

See the following guides so you can use this project to generate some reports for yourself on users or repos you are interested in. Note that these only cover the case of a Unix-style environment.

- [Aims](/aims.md) - The main purposes for this project and how they could benefit you.
- [Installation](/installation.md) - Setup project environment and configs.
- [Usage](/usage.md) - Run scripts to generate reports.
- [Datasources](/datasources.md) - Info and links around APIs.

See also GitHub's resources and samples for running GraphQL queries - [platform-samples](https://github.com/github/platform-samples/tree/master/graphql).
