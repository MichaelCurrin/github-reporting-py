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

These are not that useful for reporting, but their code is mostly self-contained so it is easy to understand how the API works in a single script or function.

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

### Repo summary reports

#### Metadata

Get metadata for all repos under a user or organization and print to the screen.

```bash
$ ./repos_about.py --help
```

Open the report.

#### Commit counts

Get the latest commit and the total commit count for all repos under a user or organization and write to a CSV.

```bash
$ ./repos_and_commit_counts.py --help
```

### Commit reports

Use the commit reports to get the _git_ commit history across multiple repos and to see how your organization or team members contribute. Don't use this _git_ reporting in isolation to judge the productivity of your team members or the activity of the codebase. These reports can help you see patterns or blockers and that can help you identify problems to solve or areas to improve on.

The CSV output is commit-level data from one or more repos. Each row in the report is a commit. The following fields are in the headers of the commit repos:

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
...
```

Example.

```bash
$ ./repo_commits.py michaelcurrin twitterverse
```

Set a start date to only get commits from that date onwards. This can make the script run much quicker if you choose a recent date.

```bash
$ ./repo_commits.py michaelcurrin twitterverse --start 2019-04-01
```

Open the report.

To update the report output, use different command-line arguments. The repo name and the start date are used in the filename, so you can run the report with different parameters and get multiple CSV reports.

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

To change the report output, update and save the config then rerun the report.


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
