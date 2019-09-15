# Datasources


## Links

- [Github GraphQL explorer](https://developer.github.com/v4/) - edit and run queries against live data, in the browser.
- [Github GraphQL resource limitations](https://developer.github.com/v4/guides/resource-limitations/)
    * > Individual calls cannot request more than 500,000 total nodes.


## Github APIs

[Github](https://github.com) hosts code for developers and organizations and makes the code and history available through APIs. Here are Github's two latest ones:

- Version 3 - A [REST](https://www.restapitutorial.com/) API
- Version 4 - A [GraphQL](https://graphql.org/) API

This project explores using the GraphQL API for reporting purposes, in particular because GraphQL is more modern and requires far fewer requests to get the same data.

You can use _curl_ or a library like Python _requests_ to do command-line requests to the API.

For easy debugging, autocompletion and exploring of the schema, use the [GraphQL explorer](https://developer.github.com/v4/explorer/).


## GraphQL benefits

Using [GraphQL](https://graphql.org/) means only a single endpoint to query, using a POST request usually to get data. It allows fetching of large amounts of data with fewer queries than REST, getting just the fields and level of detail requested. Note that paging and rate limits still apply but should be easier to deal with.

In particular, **GraphQL** makes it easier to scale to many fetch a large numbers of commits, even across multiple repos or branches, using a single request.  Although, there is a strict API limit of a **max of 100 items** in a list, so you need to use multiple requests to paginate through the data. But in a single request, you can still fetch 100 repos and the most recent 100 commits on each.

This is still much better than the **REST API**, which only lets you query one repo at a time and only gives a single commit and a pointer to the previous commit (or _commits_, for a merge). This is slow and results in quick rate limiting (max 5000 requests per hour). I experienced this in a similar previous project which used a Python wrapper on the Github REST API.

GraphQL is 100 times faster at getting commits and 100 times faster at getting repos, resulting in a gain of 10,000 times faster performance. For example, given a scenario to get 1,000 commits for the default branches of 100 repos, here are the number of requests required:

- **REST API**: 100 repos x 1000 commits for each = *100,000 requests*
- **GraphQL API**: 1 page of repos x 10 commit pages = *10 requests*
