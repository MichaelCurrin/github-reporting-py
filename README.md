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

Run the demo scripts to see sample output.

```bash
$ PYTHONPATH=$(pwd) python demo/basic.py
$ PYTHONPATH=$(pwd) python demo/parametized.py
```
