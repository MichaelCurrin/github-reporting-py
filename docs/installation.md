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
    * ☑ repo
        - Tick the top level for access to private repos. Otherwise just tick _repo:status_ and _public:repo_.
    * ☐ admin:org
        - ☑ read:org
    * ☐ write:discussion
        - ☑ read:discussion
    * ☐ user
        - ☑ read
        - ☑ email
6. Find the generated token value, which you'll use in the next step. Do not navigate away yet as the token cannot be viewed online later.

### Add token to the project

```bash
$ cd ghgql/etc
$ cp app.template.py app.local.yml
```

Open the created file with a command, or your IDE.

```bash
$ edit etc/app.local.yml
```

Paste your token value. e.g.
```yaml
access_token: ABCDEF0123456789
```

If you want to do run the commit report on configured details, fill in the commit report section now or later.

Save and exit.

You are now setup and so can continue to the [Usage](usage.md) instructions.
