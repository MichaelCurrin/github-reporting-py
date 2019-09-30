# Github GraphQL Tool
> Python tool to easily report on data fetched from Github's GraphQL API

A project to explore the Github GraphQL API for fun and to output data on repos, users and commits for reporting. 

If you came here just to look at GraphQL queries that get data from Github, see the [queries](/ghgql/queries) directory. You can paste those in Github's [GraphQL Explorer](https://developer.github.com/v4/explorer/) and run them against public data. For some queries you need to ad JSON params in the query variables section.

If you want to download the results as text or CSV files or automate the requests for many pages of data, then follow the [aims](#aims) and [documentation](#documentation) sections below to setup the project then run the command-line Python scripts to generate the reports. The scripts use the GQL queries internally.

Why GraphQL and not REST API? This project arose because of speed and rate limit issues with using the REST API for large volumes of commit data. But, the GraphQL is about **100 times faster**, in cases such as getting a page of 100 commits rather than one commit from the REST API commit endpoint. See the Datasources doc's [GraphQL benefits](/docs/datasources.md#graphql-benefits) section for more details.


## Aims

### Reporting

The aim of this project is to fetch stats about Github repos of interest and generate reports.

The GraphQL API is used to get this data at scale, which enables quick reporting on a even large Github organization or user account with many repos. This project's reports generally fetch data in a single request that otherwise take 100 or more requests to the REST API. Additionally, some of the report script in this project have pagination built in, to get data beyond the first page.

The response data is parsed and then printed on the screen or written to CSV reports.

Here is an outline of the report scripts available in this project, with links to them in usage document.

- [Demos reports](/docs/usage.md#demo-reports) - A few simple scripts.
- [Repo summary reports](/docs/usage.md#repo-summary-reports) - Get metadata about reports or counts of commits.
- [Commit reports](/docs/usage.md#commit-reports) - Get the _git_ commit history across multiple repos and to see how your organization or team members contribute.

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

- [Installation](/docs/installation.md) - Setup project environment and configs.
- [Usage](/docs/usage.md) - Run scripts to generate reports.
- [Datasources](/docs/datasources.md) - Info and links around APIs.
