# Datasources
> Information and links around GitHub API.

See [GitHub API][] in my Dev Resources for more.

[GitHub API]: https://michaelcurrin.github.io/dev-resources/resources/version-control/github/api/

This project explores using the GraphQL API for reporting purposes, since the GraphQL one is more modern and efficient than using REST. With GrapghQL, it usually requires far fewer requests to get the same data and you do not overfetch on fields you don't need).


## GraphQL benefits

Using [GraphQL](https://graphql.org/) means only a single endpoint to query, using a POST request usually to get data. It allows fetching of large amounts of data with fewer queries than REST, getting just the fields and level of detail requested. Note that paging and rate limits still apply but should be easier to deal with.

**GraphQL** makes it easy to scale to many fetch a 100 commits for a repo using a single request (due to API's limit of 100 items on a page), while using **REST API** would take 100 requests. So getting data with GraphQL is about 100 times faster. i.e. The requests done in one minute using GraphQL would take 1 hour and 40 minutes using the REST API. Getting objects from the REST API using one request at time is tedious and slow, even when using a GitHub API library. It is especially slow when getting a history of commits - GitHub's REST API only returns _one_ commit at a time (along with a URL pointing to the next commit to query).

See the report covered in the [Multiple Repos](/docs/usage.md#multiple-repos) section of the usage doc, which shows how to get pages of commits, going through multiple repos in a sequence.

You can get higher volume of commits in a single query. The breadth option of getting more repos does work, but you do not get the depth of more than 100 commits for any one repo because GQL does not support nest paging (of repos and commits). With the limited approach, you get 100 commits each for a 100 repos using the [repos_recent_commits.py](/ghgql/repos_recent_commits.py) script and associated GQL query and then to page through all repos. The script iterates through the pages so all repos can be covered.

Alternatively, you can build up the query using templating and a known list of repos. Part of this project explored this. However, loading proved problematic. The number of commits and repos had to be dropped significantly below 100 in order stop the query returning error messages probably due to GitHub's limit on resources. The lower scale of the report of 3 repos at a time with about 40 commits proved to be not that worthwhile, so the experimental feature was left unfinished.


