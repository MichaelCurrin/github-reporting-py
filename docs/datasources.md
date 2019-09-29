# Datasources

Information and links around Github datasources.

## Links

- [REST API](https://www.restapitutorial.com/) - tutorial.
- [GraphQL](https://graphql.org/) - website with tutorials.
- [Github's GraphQL explorer](https://developer.github.com/v4/) - edit and run queries against live data, in the browser.
- [Github GraphQL resource limitations](https://developer.github.com/v4/guides/resource-limitations/)
    * > Individual calls cannot request more than 500,000 total nodes.


## Github APIs

[Github](https://github.com) hosts code for developers and organizations and makes the code and history available through APIs. Here are Github's two latest ones:

- Version 3: REST API
- Version 4: GraphQL API

This project explores using the GraphQL API for reporting purposes, in particular because GraphQL is more modern and requires far fewer requests to get the same data.

You can use _curl_ or a library like Python _requests_ to do command-line requests to the API.

For easy debugging, autocompletion and exploring of the schema, use the [GraphQL explorer](https://developer.github.com/v4/explorer/).


## GraphQL benefits

Using [GraphQL](https://graphql.org/) means only a single endpoint to query, using a POST request usually to get data. It allows fetching of large amounts of data with fewer queries than REST, getting just the fields and level of detail requested. Note that paging and rate limits still apply but should be easier to deal with.

**GraphQL** makes it easy to scale to many fetch a 100 commits for a repo using a single repo (due to API's limit of 100 items on a page), while using **REST API** would take 100 requests. See the reports covered in the [Multiple Repos](/docs/usage.md#multiple-repos) section of the usage doc.

You can get higher volume of commits in a single query. The breadth option of getting more repos does work, but you do not get the depth of more than 100 commits for any one repo because GQL does not support nest paging (of repos and commits). With the limited approach, you get 100 commits each for a 100 repos using the [repos_recent_commits.py](/ghgql/repos_recent_commits.py) script and associated GQL query and then to page through all repos. The script iterates through the pages so all repos can be covered.

Alternatively, you can build up the query using templating and a known list of repos. Part of this project explored this. However, loading proved problematic. The number of commits and repos had to be dropped significantly below 100 in order stop the query returning error messages probably due to Github's limit on resources. The lower scale of the report of 3 repos at a time with about 40 commits proved to be not that worthwhile, so the experimental feature was left unfinished.


## Cursors in GraphQL

A GraphQL endpoint will limit how many items it returns to you on a page, to prevent abuse caused by requesting too many items at once.

After the first query, if there is a second page to fetch then you'll get a `'hasNextPage'` value in the paging data as `true`. And you'll get an `'endCursor'` value. Pass this cursor value in the query params payload to tell the API to skip the first page.

Then get the cursor on the second page's request and pass it to on the third request, as so on.

The cursor is specific to a query and should not be reused. It is intentionally opaque as a hashed value. In the case of Github, the hashed value component is followed by a space and number at the end. The number indicates the index of the last item on the current page, using zero based indexing.

For example:

1. Do query for page 1 with 100 items. No cursor sent.
2. Page 1 data received. Paging data includes an end cursor as something like this: `9eee3f4054dd502b105626632b15d01038a95aae 99`.
3. Do query for page 2 with 100 items. Send cursor from step above.
4. Page 2 data received. Paging data includes an end cursor as something like this: `9eee3f4054dd502b105626632b15d01038a95aae 199`.
5. Do query for page 3 and so on.
