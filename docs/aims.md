# Aims

If you want to learn about GraphQL, GraphQL + Python integration, or to do reporting on GitHub data using the GraphQL API, then this project is for you.


## GraphQL reference

If you came here just to look at GraphQL queries that get data from GitHub, see the [queries](/ghgql/queries) directory. You can paste those in GitHub's [GraphQL Explorer](https://developer.github.com/v4/explorer/) and run them against public data. For some queries you need to add JSON params in the query variables section.

If you want to download the results as text or CSV files or automate the requests for many pages of data, then follow the [documentation](#documentation) section below to setup the project then run the command-line Python scripts which generate the reports. The scripts use the GQL queries internally.

Why _GraphQL_ and not the _REST_ API? This project arose because of speed and rate limit issues with using _REST_ API for large volumes of commit data for _GitHub_. But, the _GraphQL_ API is about **100 times faster**, in many cases such as getting a page of 100 commits rather than one commit from the REST API commit endpoint. See the Datasources doc's [GraphQL benefits](/datasources.md#graphql-benefits) section for more details.

## GraphQL + Python reference

Another aim of this project is to explore how to run _GraphQL_ queries with _Python_. This work here can be used as a reference for programmers new to this area. The understanding of querying GitHub can be applied to other _GraphQL_ APIs.

No library specific to GraphQL or GitHub is used. Rather this project's scripts use Python [requests](https://requests.kennethreitz.org/en/master/) to send a query string and optional query parameters to the GraphQL API.

The project includes Python scripts and _GraphQL_ queries of varying complexity. Some reports multiple pages of data. Some accept command-line arguments. One of them reads required report data from a config file.

## Reporting

The reporting goal of this project is to fetch stats about GitHub repos of interest and then generate reports.

The GraphQL API is used to get this data at scale, which enables quick reporting on a even large GitHub organization or user account with many repos. This project's reports generally fetch data in a single request that otherwise take 100 or more requests to the REST API. Additionally, some of the report script in this project have pagination built in, to get data beyond the first page.

The response data is parsed and then printed on the screen or written to CSV reports.

See the [usage](/usage.md) page for details on what reports you get.
