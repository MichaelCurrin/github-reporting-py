# Installation


## Setup environment

This project requires you to setup Python 3 as well as a Python virtual environment, with the project's packages installed into it. 

To set those up for this project (or similar Python projects), follow the instructions here in my [gist](https://gist.github.com/MichaelCurrin/3a4d14ba1763b4d6a1884f56a01412b7). Then continue below.


## Configure project

This project requires a valid Github API _access token_ in order to authenticate with the API for requests. Create your access token in your Github account settings. Ensure it has access to read repo details. Save the private token somewhere. Include the token in this project using instructions below.

```bash
$ cd ghgql
$ cp config_local.template.py config_local.py
```

Open the created file with a command, or your IDE.

```bash
$ edit config_local.py
```

Paste your token value, then save and exit.


You are now setup and so can continue to the [Usage](usage.md) instructions.
