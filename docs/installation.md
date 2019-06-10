# Installation

## Setup environment

The project requires only Python 3 and virtual environment. Follow the instructions in my [gist](https://gist.github.com/MichaelCurrin/3a4d14ba1763b4d6a1884f56a01412b7).

## Configure project

This project requires a valid Github API access token in order to authenticate with the API for requests.

Create your access token in your Github account settings. Ensure it has access to read repo details. Save the private token somewhere. Include the token in this project using instructions below.

```bash
$ cd ghgql
$ cp config_local.template.py config_local.py
```

Open the created file with a command, or your IDE.

```bash
$ edit config_local.py
```

Paste your token value, then save and exit.
