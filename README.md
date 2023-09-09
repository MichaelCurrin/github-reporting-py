# GitHub Reporting Tool 👨‍💻 📊 🐍

> Create detailed and summary CSV reports of activity by a GitHub user, using the GraphQL API

[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/github-reporting-py)](https://github.com/MichaelCurrin/github-reporting-py/tags/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#license)

[![Made with Python](https://img.shields.io/badge/Python->=3.9-blue?logo=python&logoColor=white)](https://python.org)
[![API - GitHub GraphQL](https://img.shields.io/badge/GitHub_API-V4_GraphQL-blue?logo=github)](https://graphql.github.io/)

## Quick start

Say you just want to get a CSV file of all your commits on the deafult branch of a repo.

1. `cd ghgql`
2. Set your GitHub access token in `etc/app.local.yml`
3. Run `python config.py`
4. Run your commit query via

```bash
python repo_commits.py REPO_OWNER REPO_NAME COMMITTER -o OUTPUT_DIR -s START_DATE -e END_DATE
```

This app is currently limited to querying commits from the default branch of a repo.

## Purpose

This tool was created to:

- **Explore** the GitHub GraphQL API for fun.
- Output CSV **reports** around repos, users and commits - all within a target GH user or organization.
- Act as a **wrapper** on requests and formatting, so you can focus on writing or using a query and getting the data out as a CSV.
- Act an easy CLI for anyone - without caring about what language the tool is implemented in (other than installing initially).

## Documentation

<div align="center">

[![View docs](https://img.shields.io/badge/View-Online_docs-blue?style=for-the-badge)](https://michaelcurrin.github.io/github-reporting-py/ "Go to docs site")

</div>

## Contributing

If you want to make the project better, see the [contribution guidelines](/CONTRIBUTING.md).

## License

Released under [MIT](/LICENSE) by [@MichaelCurrin](https://github.com/MichaelCurrin/).
