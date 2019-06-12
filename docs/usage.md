
# Usage

```bash
$ cd <PATH/TO/REPO>
$ source venv/bin/activate
$ cd ghgql
```


## Run demos

Run the simple demo scripts. These are not that useful for reporting, but their code is mostly self-contained so it is easy to understand the querying the API works, with and without query variables in the payload.

```bash
$ PYTHONPATH=$(pwd) python demo/basic.py
$ PYTHONPATH=$(pwd) python demo/variables.py
```


## Run a report

Run the [query script](/ghgql/query.py) which will execute a given file containing a valid Github GraphQL query. See available input queries in the [queries](/ghgql/queries) directory.

### Static

Run a GraphQL query by filename. Choose a static one, that always gives the same output as it has no variables.

Example:

```bash
$ python query.py queries/commits/first_page.gql
```

### Dynamic

Run a specific query that needs variables. Provide key-value pairs separated by spaces.

Example:

```bash
# You can view the query text first, to see what variables are needed. As you will get
# an API error printed to the console if you omit a required variable.
$ view queries/commits/parametized.gql
$ python query.py queries/commits/parametized.gql owner michaelcurrin name aggre-git
```

Since the API allows a max of 100 items on page, paginate through the pages of results. The "after" indicator for the next page is added internally to the variables sent in the payload, so paging will happen automatically.

Example - this is fixed to use a single query.

```bash
$ python paginate_demo.py
```
