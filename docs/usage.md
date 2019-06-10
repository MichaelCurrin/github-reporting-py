
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

For example:

```bash
$ python query.py queries/commits.gql
```
