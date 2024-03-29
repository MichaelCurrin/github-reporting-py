#!/usr/bin/env python
"""
Read counts script.

Read an existing CSV of repo counts and return.

If this script is run alone, the contents of the CSV are printed out with some
pretty formatting. Make sure `repos_and_commit_counts.py` has been run first.
"""
import lib


def read(start=None):
    """
    Read CSV, order by oldest first, parse last committed date then return.

    If start is set with a datetime.date object, then filter results to only
    that date or after.

    Remove any rows for empty repos.
    """
    repo_count_data = lib.read_csv(lib.COUNTS_CSV_PATH_TODAY)

    repo_count_data.sort(key=lambda x: x["last_committed_date"])

    out_data = []

    for row in repo_count_data:
        if row["branch_name"]:
            last_committed_date_str = row["last_committed_date"]

            if last_committed_date_str:
                last_committed_date = lib.time.as_date(last_committed_date_str)
            else:
                last_committed_date = None

            if start is None or last_committed_date >= start:
                row["last_committed_date"] = last_committed_date

                out_data.append(row)

    return out_data


def repo_names(start=None):
    """
    Return CSV data as owner name and list of repo names.
    """
    repos_summary = read(start)

    owner_name = repos_summary[0]["owner_name"]

    return owner_name, [r["repo_name"] for r in repos_summary]


def test():
    """
    Test the read and repo_names functions.
    """
    rows = read()
    print(f"Total: {len(rows)}")
    print()

    preview = 3
    print(f"Latest {preview} rows")

    for row in rows[(-1 * preview) :]:
        for k, v in row.items():
            print(f"{k:23}: {v}")
        print()

    print("repo_names")
    owner, names = repo_names()
    print(owner, len(names))


if __name__ == "__main__":
    test()
