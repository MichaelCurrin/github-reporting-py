
# Usage

Activate the virtual environment and navigate to the app directory.

```bash
$ cd <PATH/TO/REPO>
$ source venv/bin/activate
$ cd ghgql
```

If you use VSCode and open a terminal after the Python Extension has loaded, this will be done for you because of the configs in this repo.


## Run demos

Run the simple demo scripts. These are not that useful for reporting, but their code is mostly self-contained so it is easy to understand the querying the API works, with and without query variables in the payload.

```bash
$ PYTHONPATH=$(pwd) python demo/basic.py
$ PYTHONPATH=$(pwd) python demo/variables.py
```

## Run featured reports

### Commit reports

This is the main purpose of this project - do producer CSV reports on one or more repos using an optional start date.

The reports are saved to the [var](/ghgql/var) directory. A filename will be shown in the printed output.


#### Single repo

Run a report for a single repo using details on the command line.

```bash
$ ./repo_commits.py --help
usage: repo_commits.py [-h] [-s DATE] OWNER REPO_NAME

...
```

Example without start date.
```bash
$ ./repo_commits.py michaelcurrin twitterverse
```

Example with start date.
```bash
$ ./repo_commits.py michaelcurrin twitterverse --start 2019-04-01
```

Open the report.


#### Multiple repos

Set the details in the `etc/app.local.yml` file's commit report section, if not set already.


For example:

- Get commits from a start date up to today, for one repo.
    ```yaml
    commit_report:
      start_date: 2019-09-01
      owner: michaelcurrin
      repo_names:
      - twitterverse
    ```
- Get commits from 30 days ago up to today, for multiple repos.
    ```yaml
    commit_report:
      start_date: 30
      owner: michaelcurrin
      repo_names:
      - twitterverse
      - github-graphql-tool
    ```

Run the report, with no arguments.

```bash
$ ./repo_commits_from_conf.py
```

Open the report.


### Run other reports

Run the [query script](/ghgql/query.py) which will execute a given file containing a valid Github _GraphQL_ query. See available input queries in the [queries](/ghgql/queries) directory.

#### Static

Run a GraphQL query by filename. Choose a static one, that always gives the same output as it has no variables.

Example:

```bash
$ python query.py queries/commits/first_page.gql
```

#### Dynamic

Run a specific query that needs variables. Provide key-value pairs separated by spaces.

Example:

```bash
# You can view the query text first, to see what variables are needed. As you will get
# an API error printed to the console if you omit a required variable.
$ view queries/commits/parametized.gql
$ python query.py queries/commits/parametized.gql owner michaelcurrin name twitterverse
```

Since the API allows a max of 100 items on page, paginate through the pages of results. The "after" indicator for the next page is added internally to the variables sent in the payload, so paging will happen automatically.

Example - this is fixed to use a single query.

```bash
$ python paginate_demo.py
```
