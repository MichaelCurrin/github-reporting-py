# Datasources

Information and links around Github datasources.

## Github APIs

[Github](https://github.com) hosts code for developers and organizations and makes the code and history available through APIs. Here are Github's two latest ones:

- V3 REST API
- V4 GraphQL

This project explores using the GraphQL API for reporting purposes, in particular since the GraphQL one is more modern and efficient (it usually requires far fewer requests to get the same data and you do not overfetch on fields you don't need).

You can use _curl_ or a library like Python _requests_ to do command-line requests to the API.

For easy debugging, autocompletion and exploring of the schema, use the [GraphQL explorer](https://developer.github.com/v4/explorer/).

### Links

#### REST API

- Version: 3
- API URL: `api.github.com/` 
    - Do GET requests against the many endpoints here. 
    - e.g. `GET /repos/octokit/octokit.rb`.
    - Defaults to `/v3/` so you do not need to specify that.
- [V3 Docs](https://developer.github.com/v3/)

#### GraphQL API

- Version: 4
- API URL: `api.github.com/graphql`
    - Do POST requests against this single endpoint.
- [Explorer](https://developer.github.com/v4/explorer/) 
    - edit and run queries against live data, in the browser. Requires you to sign in.
- [V4 Docs](https://developer.github.com/v4/)
- [Resource limitations](https://developer.github.com/v4/guides/resource-limitations/)
    * > Individual calls cannot request more than 500,000 total nodes.

### Tutorials

- [REST API](https://www.restapitutorial.com/)
- [GraphQL](https://graphql.org/)


## GraphQL benefits

Using [GraphQL](https://graphql.org/) means only a single endpoint to query, using a POST request usually to get data. It allows fetching of large amounts of data with fewer queries than REST, getting just the fields and level of detail requested. Note that paging and rate limits still apply but should be easier to deal with.

**GraphQL** makes it easy to scale to many fetch a 100 commits for a repo using a single request (due to API's limit of 100 items on a page), while using **REST API** would take 100 requests. So getting data with GraphQL is about 100 times faster. i.e. The requests done in one minute using GraphQL would take 1 hour and 40 minutes using the REST API. Getting objects from the REST API using one request at time is tedious and slow, even when using a Github API library. It is especially slow when getting a history of commits - Github's REST API only returns _one_ commit at a time (along with a URL pointing to the next commit to query).

See the report covered in the [Multiple Repos](/docs/usage.md#multiple-repos) section of the usage doc, which shows how to get pages of commits, going through multiple repos in a sequence.

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
