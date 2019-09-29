# Github GraphQL Tool
> Python tool to easily report on data fetched from Github's GraphQL API

## Aims

### Reporting

The aim of this project is to fetch stats about Github repos of interest and to generate text or CSV reports, using input parameters.

The GraphQL API is used to get this data at scale, which makes reporting on a large Github organization easy.

Many of the reports in this project can do a single request to get data that otherwise take 100 or more requests to the REST API. Additionally, some of the report script in this project have pagination built into get data beyond the first page.

#### Commit reports

View the _git_ commit history across multiple repos and to see how your organization or team members contribute. However, don't use this _git_ reporting in isolation to judge the productivity of your team members or the activity of the codebase. These reports can help you see patterns or blockers and that can help you identify problems to solve or areas to improve on.

See the [Commit reports](/docs/usage.md#commit-reports) section of the Usage doc to run reports.

#### Repo summary reports

Get metadata about reports or counts of commits.

See the [Repo summary reports](/docs/usage.md#repo-summary-reports) section of the Usage doc to run reports.


### Python-GraphQL Reference

Another aim of this project is to explore how to run _GraphQL_ queries with _Python_. This work here can be used as a reference for programmers new to this area. The understanding of querying Github can be applied to other _GraphQL_ APIs.

No library specific to GraphQL or Github is used. Rather this project's scripts use Python [requests](https://requests.kennethreitz.org/en/master/) to send a query string and optional query parameters to the GraphQL API.

The project includes Python scripts and _GraphQL_ queries of varying complexity. Some reports multiple pages of data. Some accept command-line arguments. One of them reads required report data from a config file.


## Project Requirements

You need the following to run this project:

- Github account
- Github API token with access to repos
- Internet connection
- Python 3.6+


## Documentation

See the following guides so you can use this project to generate some reports for yourself on users or repos you are interested in. Note that these only cover the case of a Unix-style environment.

- [Installation](/docs/installation.md) - get setup
- [Usage](/docs/usage.md) - run reports
- [Datasources](/docs/datasources.md) - info and links around APIs
