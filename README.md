# Github GraphQL Tool
> Python tool for easy requests to the Github API V4 GraphQL endpoint

The documentation is intended for installing and running on a Unix-style environment.

## Installation

The project requires only Python 3 and virtual environment. Follow the instructions in my [gist](https://gist.github.com/MichaelCurrin/3a4d14ba1763b4d6a1884f56a01412b7).


## Usage

```bash
$ cd <PATH/TO/REPO>
$ source venv/bin/activate
$ cd ghgql
```


### Demo

Run the simple demo scripts. These are not that useful for reporting, but their code is mostly self-contained so it is easy to understand the querying the API works.

```bash
$ PYTHONPATH=$(pwd) python demo/basic.py
$ PYTHONPATH=$(pwd) python demo/parametized.py
```

### Run a query

Run the [query script](ghql/query.py) which will execute a given file containing a valid Github GraphQL query.

For example:

```bash
$ python query.py queries/commits.gql
```
