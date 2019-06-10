
# Usage

```bash
$ cd <PATH/TO/REPO>
$ source venv/bin/activate
$ cd ghgql
```


## Run demos

Run the simple demo scripts. These are not that useful for reporting, but their code is mostly self-contained so it is easy to understand the querying the API works.

```bash
$ PYTHONPATH=$(pwd) python demo/basic.py
$ PYTHONPATH=$(pwd) python demo/parametized.py
```


## Run a report

Run the [query script](ghql/query.py) which will execute a given file containing a valid Github GraphQL query.

### Static

Run specific query that does not take variables.

Example:

```bash
$ python query.py queries/commits.gql
```

### Dynamic

Run a specific query that needs variables. Provide key-value pairs separated by spaces.

Example:

```bash
# You can view the query text first, to see what variables are needed. As you will get
# an API error printed to the console if you omit a required variable.
$ view queries/commits_parametized.gql
$ python query.py queries/commits_parametized.gql owner michaelcurrin name aggre-git
```
