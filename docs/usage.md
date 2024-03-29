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
$ cd PATH_TO_REPO
$ source venv/bin/activate
$ cd ghgql
```

Note: If you use the _VS Code_ IDE and open a terminal _after_ the Python Extension has loaded, this will be done for you because of the configs that come with this project.


## Paging note

Note that for API results, GitHub usually limits the page to have up to 100 items (such as repos or users). This is adjusted with the `first` variable. To next beyond the first page, using the `after` variable with a cursor value.

For some queries in this project, this is not handled at all, or requires a manually set cursor.

However, some parts of this project handled this automatically. Such as the the repo and commit reports, where you just input the data you need (with optional date range to make it quicker) and the script will get all pages of data available before writing to a CSV.


## Demo reports

Run the simple demo scripts, which take no inputs or configs (other than the access token). These showcase querying the GraphQL and printing the JSON responses to the screen.

These are not that useful for reporting, but their code is mostly self-contained so it is easy to understand how the API works in a single script or function.

- This runs without variables in the request payload.
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
- Run all of demos at once. From the repo root:
    ```bash
    $ make demo
    ```


## Query runner

This project has a query runner Python script that lets you execute **arbitrary GQL queries** and print the results. This makes it great for testing the query itself. All you need is the path to the `.gql` file and configured GitHub credentials.

The result of the GQL output will be printed to the console as pretty JSON - this can be redirected to a file somewhere to store the data. The main limitation here is that the script does not understand the structure of the queries or results, so therefore the results cannot be converted to CSV output.

Here are are advantages of this approach over using the GQL explorer in the browser:

- Easily run a new or modified query which is in the repo. No need to copy and paste queries.
- Easily change variables for the query. No without worrying about JSON syntax. Also, dates are converted to proper GitHub datetime types.
- Get the results outputted to the console.
- Optionally store results as a file.

A page cursor can be passed on the command-line. For future development, extend this to handle multiple pages automatically. See GitHub [issue #5](https://github.com/MichaelCurrin/github-reporting-py/issues/5).

### How to run

Instructions are covered below for how to do this with the `ghgql/query.py`. The file path would usually be to a `.gql` file in the `ghgql/queries` directory, though it can point to anywhere.

See the script's instructions:

```bash
$ ./query.py --help
```

Simple usage just requires the path to query as a text file. Variables can be set as key-value pairs, if the query use variables.

### Examples

Example with no variables set. The result will be printed.

```bash
$ ./query.py queries/commits/first_page.gql
```

Here the result will be stored as a JSON file.

```bash
$ ./query.py queries/commits/first_page.gql > var/my_report.json
```

Example with variables provided as key-value pairs, separated by spaces. Just prints the results to the console.

```bash
$ ./query.py queries/commits/parametrized.gql owner michaelcurrin name twitterverse
```


## CSV Reports

This is the main purpose of this project is to produce CSV reports about repos. The reports are saved to the `ghgql/var` directory. A filename will be shown in the printed output.

### Repo summary reports

#### Metadata

Get metadata for all repos under a user or organization and print to the screen.

```bash
$ ./repos_about.py --help
```

After running, open the report.

#### Commit counts

This command will go through a user or org and get a count of commits in each repo. The latest commit is also included. The result is written to a CSV.

- [repos_and_commit_counts.py](https://github.com/MichaelCurrin/github-reporting-py/blob/master/ghgql/repos_and_commit_counts.py)

```bash
$ ./repos_and_commit_counts.py --help
```
```
Usage: ./repos_and_commit_counts.py owner OWNER [start START_DATE]
START_DATE: Count commits on or after this date, in YYYY-MM-DD format. This only affects the commit count and not whether the repo is shown
```

Examples:

```bash
$ ./repos_and_commit_counts.py owner MichaelCurrin
```

Or

```bash
$ ./repos_and_commit_counts.py owner MichaelCurrin start 2020-04-01
```

Then open the report.

### Commit reports

Use the commit reports to get the _git_ commit history across multiple repos and to see how your organization or team members contribute. Don't use this _git_ reporting in isolation to judge the productivity of your team members or the activity of the codebase. These reports can help you see patterns or blockers and that can help you identify problems to solve or areas to improve on.

The CSV output is commit-level data from one or more repos. Each row in the report is a commit.

The following fields are in the headers of the commit repos:

| Field             | Description                                                                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `repo_name`       | Name of repo where the commit was made.                                                                                                         |
| `branch_name`     | Name of branch where the commit was made.                                                                                                       |
| `commit_id`       | Short commit hash.                                                                                                                              |
| `author_date`     | Date the commit was _authored_ (originally written).                                                                                            |
| `author_login`    | Username of the author (who originally wrote the commit).                                                                                       |
| `committed_date`  | Date the commit was _committed_. You probably want to use the author fields above rather than these commit fields but they are provided anyway. |
| `committer_login` | Username of the commit's committer.                                                                                                             |
| `changed_files`   | Number of files changed.                                                                                                                        |
| `additions`       | Number of lines added.                                                                                                                          |
| `deletions`       | Number of lines removed.                                                                                                                        |
| `message`         | Commit message.                                                                                                                                 |

A further note on _author_ vs _committer_ for a commit:

- Details for shown in the report output for both, for the most flexibility. They are usually the _same_ person, but, sometimes one username can be different or one field can be missing.
- In the case of a merged Pull Request, _both_ login fields could be blank, though there is still a date repeated in both date columns.

An explanation from the [commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History) part of the _git_ docs:

> You may be wondering what the difference is between author and committer. The author is the person who originally wrote the work, whereas the committer is the person who last applied the work. So, if you send in a patch to a project and one of the core members applies the patch, both of you get credit — you as the author, and the core member as the committer.

You can run the Python script with command-line arguments to get data for a single repo, or use another script and the app config file to get data for multiple repos.

#### Single repo report

Run a report for a single repo using details passed on the command line.

- [repo_commits.py](/ghgql/repo_commits.py)

```bash
$ ./repo_commits.py --help
```

Example:

```bash
$ ./repo_commits.py michaelcurrin github-reporting-py
```

Set a start date to only get commits from that date onwards. This can make the script run much quicker if you choose a recent date. Example:

```bash
$ ./repo_commits.py michaelcurrin github-reporting-py --start 2019-04-01
```

Open the report.

To update the report output, use different command-line arguments. The repo name and the start date are used in the filename, so you can run the report with different parameters and get multiple CSV reports.

#### Multiple repos report

Run a CSV report against named repos in a user or org, with optional start date. This script makes it easy to run a report repeatedly as it uses a config as an input rather than command-line options.

- [repos_commits_from_conf.py](https://github.com/MichaelCurrin/github-reporting-py/blob/master/ghgql/repos_commits_from_conf.py)

First set the details in the `etc/app.local.yml` file's commit report section, if not set already.

For example:

- Get commits from a start date up to today, for one repo.
    ```yaml
    commit_report:
      start_date: 2019-09-01
      owner: michaelcurrin
      repo_names:
        - github-reporting-py
    ```
- Get commits from 30 days ago up to today, for multiple repos.
    ```yaml
    commit_report:
      start_date: 30
      owner: michaelcurrin
      repo_names:
        - github-reporting-py
        - twitterverse
    ```

Run the report script - no arguments needed.

```bash
$ ./repos_commits_from_conf.py
```

Open the CSV reports.

The one is on commit-level data and the other rolls commits up to repo names - this was extra functionality added later which is a commit count not just commits report. Note that files changed column would be overestimated as it adds up across commits so only lines changed and number of commits is accurate and useful here.

To change the report output, update and save the config then rerun the report.

#### Daily commit counts

- [daily_commit_counts.py](https://github.com/MichaelCurrin/github-reporting-py/blob/master/ghgql/daily_commit_counts.py)

Usage - persist as a CSV file.

```bash
$ ./daily_commit_counts.py > var/daily.csv
```

?> Currently this does not take any parameters. It just looks up activity for the current user, from 2015 to 2021 inclusive.

Sample result:

| date       | contributions |
| ---------- | ------------- |
| 2015-01-01 | 2             |
| 2015-01-02 | 0             |
| ...        | ...           |
| 2019-03-28 | 4             |
| 2019-03-29 | 6             |
| 2019-03-30 | 8             |
| 2019-03-31 | 0             |
| ...        | ...           |
| 2021-07-24 | 17            |
| 2021-07-25 | 60            |
