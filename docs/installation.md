# Installation


## Setup environment

This project requires you to setup Python 3 as well as a Python virtual environment, with the project's packages installed into it.

To set those up for this project (or similar Python projects), follow the instructions here in my [gist](https://gist.github.com/MichaelCurrin/3a4d14ba1763b4d6a1884f56a01412b7). Then continue below.


## Configure project

### Create a token

This project requires a valid Github API _access token_ in order to authenticate with the API for requests.

Create your access token in your Github account settings. Ensure it has access to read repo details.

1. Open Github and login.
2. Go to [OAuth Apps](https://github.com/settings/developers).
3. Create an app. e.g. "Git Reporting".
4. Go to the [Tokens](https://github.com/settings/tokens) page.
5. Create a new token. The following scopes are recommended to be set:
    * ☑ `repo`
        - Tick the top level for access to _private_ repos. If you are fine with just public repos, then just tick `repo:status` and `public:repo`.
    * ☐ `admin:org`
        - ☑ `read:org`
    * ☐ `write:discussion`
        - ☑ `read:discussion`
    * ☐ `user`
        - ☑ `read`
        - ☑ `email`
6. Find the generated token value, which you'll use in the next step. Do not navigate away yet,as the token **cannot** be viewed online later. You can generate a new value for the token anytime and that will make the old value inactive.

### Add token to the project

```bash
$ cd ghgql/etc
```

Create a local config using the template.

```bash
$ cp app.template.py app.local.yml
```

Open the created file with a command, or your IDE.

```bash
$ edit app.local.yml
# VS Code
$ code app.local.yml
```

Paste your Github token value, without quotes e.g.

```yaml
access_token: ABCDEF0123456789
```

Leave the other section as is for now.

Save and exit.

You are now setup and so can continue to the [Usage](usage.md) instructions.
