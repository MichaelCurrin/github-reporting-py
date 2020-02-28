# Usage

Follow in the instructions in this section to run the scripts in this project.

**Reports**

- [Demo reports](#demo-reports) - A few simple scripts which demonstrate how doing queries and processing results work. The content of the results is of limited value.
- [Query runner](#query-runner) - Run arbitrary GQL queries with variables then view or store the output.
- [CSV Reports](#csv-reports)
    - [Repo summary reports](#repo-summary-reports) - Get metadata about reports or counts of commits.
    - [Commit reports](#commit-reports) - Get the _git_ commit history across multiple repos and to see how your organization or team members contribute.

## Environment

Before running scripts in the usage guide, activate the virtual environment then navigate to the app directory.

```bash
$ cd <PATH/TO/REPO>
$ source venv/bin/activate
$ cd ghgql
```

Note: If you use the _VS Code_ IDE and open a terminal _after_ the Python Extension has loaded, this will be done for you because of the configs that come with this project.

## Paging note

Note that for API results, Github usually limits the page to have up to 100 items (such as repos or users). This is adjusted with the `first` variable. To next beyond the first page, using the `after` variable with a cursor value.

For some queries in this project, this is not handled at all, or requires a manually set cursor.

However, some parts of this project handled this automatically. Such as the the repo and commit reports, where you just input the data you need (with optional date range to make it quicker) and the script will get all pages of data available before writing to a CSV.

## Demo reports

Run the simple demo scripts, which take no inputs or configs (other than the access token). These showcase querying the GraphQL and printing the JSON responses to the screen.

These are not that useful for reporting, but their code is mostly self-contained so it is easy to understand how the API works in a single script or function.

- This uses no variables in the request payload.
    ```bash
    $ python -m demo.basic
    ```
- This does send variables (in JSON format) on request payload. They are just hardcoded for purposes of keeping this script simple.
    ```bash
    $ python -m demo.variables
    ```
- Demo of pagination - get multiple pages of data. Just uses one import in order to handle reading a query and sending variables with payload to the API.
    ```bash
    $ python -m demo.paginate
    ```

## Query runner

This project has a query runner Python script that lets you execute **arbitrary GQL queries** and print the results. This makes it great for testing the query itself. All you need is the path to the `.gql` file and configured Github credentials.

The result of the GQL output will be printed to the console as pretty JSON - this can be redirected to a file somewhere to store the data. The main limitation here is that the script does not understand the structure of the queries or results, so therefore the results cannot be converted to CSV output.

Here are are advantages of this approach over using the GQL explorer in the browser:

- Easily run a new or modified query which is in the repo. No need to copy and paste queries.
- Easily change variables for the query. No without worrying about JSON syntax. Also, dates are converted to proper Github datetime types.
- Get the results outputted to the console.
- Optionally store results as a file.

A page cursor can be passed on the command-line. For future development, extend this to handle multiple pages automatically. See Github [issue #5](https://github.com/MichaelCurrin/github-graphql-tool/issues/5).

### How to run

Instructions are covered below for how to do this with the `ghgql/query.py`. The file path would usually be to a `.gql` file in the `ghgql/queries` directory, though it can point to anywhere.

See the script's instructions.

```bash
$ ./query.py --help
```

Simple usage just requires the path to query as a text file. Variables can be set as key-value pairs, if the query use variables.

### Examples

Example with no variables set. The result is printed.

```bash
$ ./query.py queries/commits/first_page.gql
```

The result is stored as a JSON file.

```bash
$ ./query.py queries/commits/first_page.gql > var/my_report.json
```

Example with variables provided as key-value pairs, separated by spaces. Just print the results to the console.

```bash
$ ./query.py queries/commits/parametized.gql owner michaelcurrin name twitterverse
```


## CSV Reports

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

Open the report.

### Commit reports

Use the commit reports to get the _git_ commit history across multiple repos and to see how your organization or team members contribute. Don't use this _git_ reporting in isolation to judge the productivity of your team members or the activity of the codebase. These reports can help you see patterns or blockers and that can help you identify problems to solve or areas to improve on.

The CSV output is commit-level data from one or more repos. Each row in the report is a commit.

The following fields are in the headers of the commit repos:

- `repo_name`: Name of repo where the commit was made.
- `branch_name`:  Name of branch where the commit was made.
- `commit_id`: Short commit hash.
- `author_date`: Date the commit was _authored_ (originally written).
- `author_login`: Username of the author (who originally wrote the commit).
- `committed_date`: Date the commit was _committed_. You probably want to use the author fields above rather than these commit fields but they are provided anyway.
- `committer_login`: Username of the commit's committer.
- `changed_files`: Number of files changed.
- `additions`: Number of lines added.
- `deletions`: Number of lines removed.
- `message`: Commit message.

A further note on _author_ vs _committer_ for a commit - details for shown in the report output for both, for the most flexibility. They are usually the same person, but sometimes one username can be different or one can be be missing. In the case of a merged Pull Request, both login fields can be blank, though there is still a date repeated in both date columns.

An explanation from the [commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History) part of the _git_ docs:

> You may be wondering what the difference is between author and committer. The author is the person who originally wrote the work, whereas the committer is the person who last applied the work. So, if you send in a patch to a project and one of the core members applies the patch, both of you get credit — you as the author, and the core member as the committer.

You can run the Python script with command-line arguments to get data for a single repo, or use another script and the app config file to get data for multiple repos.

#### Single repo report

Run a report for a single repo using details passed on the command line.

```bash
$ ./repo_commits.py --help
```

Example:

```bash
$ ./repo_commits.py michaelcurrin github-graphql-tool
```

Set a start date to only get commits from that date onwards. This can make the script run much quicker if you choose a recent date. Example:

```bash
$ ./repo_commits.py michaelcurrin github-graphql-tool --start 2019-04-01
```

Open the report.

To update the report output, use different command-line arguments. The repo name and the start date are used in the filename, so you can run the report with different parameters and get multiple CSV reports.

#### Multiple repos report

Set the details in the `etc/app.local.yml` file's commit report section, if not set already.

For example:

- Get commits from a start date up to today, for one repo.
    ```yaml
    commit_report:
      start_date: 2019-09-01
      owner: michaelcurrin
      repo_names:
        - github-graphql-tool
    ```
- Get commits from 30 days ago up to today, for multiple repos.
    ```yaml
    commit_report:
      start_date: 30
      owner: michaelcurrin
      repo_names:
        - github-graphql-tool
        - twitterverse
    ```

Run the report script without arguments.

```bash
$ ./repos_commits_from_conf.py
```

Open the CSV report.

To change the report output, update and save the config then rerun the report.
