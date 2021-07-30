# Installation


## Install system dependencies

Install Python 3 - follow this [gist](https://gist.github.com/MichaelCurrin/3a4d14ba1763b4d6a1884f56a01412b7) for assistance.


## Install project packages

Create a virtual environment.

```sh
$ cd path-to-repo
$ python3 -m venv venv
```

?> Here using Python 3's built-in `venv` module. Note that the `virtualenv` is deprecated.

Activate it.

```sh
$ source venv/bin/activate
```

Install packages into it.

```sh
$ make install install-dev
```


## Configure project

### Create a token

This project requires a valid GitHub API _access token_ in order to authenticate with the API for requests.

Create your access token in your GitHub account settings. Ensure it has access to read repo details.

1. Go GitHub and login.
2. Go to the [Personal Access Tokens](https://github.com/settings/tokens) page under Developer Settings.
3. Create a new token with appropriately scoped permissions.
    - Only **read** access is needed for this project.
    - The scopes needed depends on what you want to query. Some recommended scopes are:
        * ☐ `repo` (Optionally tick the top-level one for access to _private_ repos)
            - ☑ `public_repo`
        * ☐ `admin:org`
            - ☑ `read:org`
        * ☐ `write:discussion`
            - ☑ `read:discussion`
        * ☐ `user`
            - ☑ `read`
            - ☑ `email`
4. Find the generated token value, which you'll use in the next step.
    - Do not navigate away yet,as the token **cannot** be viewed online later. You can generate a new value for the token anytime and that will make the old value inactive.

### Add a token to the config

1. Create a local _unversioned_ config file, based on the template.
    ```bash
    $ make config
    ```
1. Open it.
    - The new file should open automatically in your default editor.
    - Or open with VS Code.
        ```sh
        $ code ghgql/etc/app.local.yml
        ```
1. Paste in your GitHub token value in `access_token`. Without quotes. Leave the other section as is, for now.
1. Save and exit.

You are now setup and so can continue to the [Usage](usage.md) instructions.
