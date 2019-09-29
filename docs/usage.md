# Usage

Follow in the instructions in this section to run the scripts in this project.

## Activate environment

Activate the virtual environment and navigate to the app directory.

```bash
$ cd <PATH/TO/REPO>
$ source venv/bin/activate
$ cd ghgql
```

Note: If you use the _VS Code_ IDE and open a terminal _after_ the Python Extension has loaded, this will be done for you because of the configs that come with this project.


## Demos reports

Run the simple demo scripts, which take no inputs or configs (other than access token). They showcase querying the GraphQL and printing the JSON responses to the screen.

These are not that useful for reporting, but their code is mostly self-contained so it is easy to understand the querying the API works.

- This uses no variables in the request payload.
    ```bash
    $ python -m python demo.basic
    ```
- This does send variables (in JSON format) on request payload. They are just hardcoded for purposes of keeping this script simple.
    ```bash
    $ python -m demo.variables
    ```
- Demo of pagination - get multiple pages of data.
    ```bash
    $ python paginate_demo.py
    ```

## Main reports

This is the main purpose of this project is to produce CSV reports about repos. The reports are saved to the [var](/ghgql/var) directory. A filename will be shown in the printed output.

### About repos report

Get metadata and commit count for all repos in an organization. This uses paging, so if you organization has 1000 repos, it will take 10 requests to get each page of 100 repos.

```bash
$ ./repos_about.py --help
```

For example:

```bash
$ ./repos_about.py michaelcurrin
```

Open the report.

### Commit reports

Get commit-level data from one or more repos. Each row in the report is a commit. The following fields are in the headers of the commit repos.

- `repo_name`: Name of repo where the commit was made.
- `branch_name`:  Name of branch where the commit was made.
- `commit_id`: Short commit hash.
- `author_date`: Date the commit was _authored_. This usually the same as the _committed_ date, but not always and sometimes one of the two can be missing.
- `author_login`: Username of the commit's author.
- `committed_date`: Date the commit was _committed_.
- `committer_login` : Username of the commit's committer.
- `changed_files`: Number of files changed.
- `additions`: Number of lines added.
- `deletions`: Number of lines removed.
- `message`: Commit message.

You can run the Python script with command-line arguments to get data for a single repo, or use another script and the app config file to get data for multiple repos.

#### Single repo

Run a report for a single repo using details on the command line.

```bash
$ ./repo_commits.py --help
usage: repo_commits.py [-h] [-s DATE] OWNER REPO_NAME

...
```

Example.

```bash
# ./repo_commits.py OWNER         REPO_NAME
$ ./repo_commits.py michaelcurrin twitterverse
```

Set a start date to only get commits from that date onwards. This can make the script run much quicker if you choose a recent date.

```bash
# ./repo_commits.py OWNER         REPO_NAME    --start DATE
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


### Experimental scripts

Run the [query.py](/ghgql/query.py) script along with the path of target queries form the [queries](/ghgql/queries) directory.

You can view the query text first, to see what variables are needed. As you will get an API error printed to the console if you omit a required variable.

The output will be printed to the console.

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
$ python query.py queries/commits/parametized.gql owner michaelcurrin name twitterverse
```

Since the API allows a max of 100 items on page, paginate through the pages of results. The "after" indicator for the next page is added internally to the variables sent in the payload, so paging will happen automatically.
