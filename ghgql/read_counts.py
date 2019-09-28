"""
Read counts script.

Read the repos and counts CSV and return data.
"""
import lib


def read(start=None):
    """
    Read CSV, order by date, parse date then return.

    If start is set datetime.date object, then filter results to only that date
    or after.

    Remove any rows for empty repos.
    """
    repo_count_data = lib.read_csv(lib.COUNTS_CSV_PATH_TODAY)

    repo_count_data.sort(key=lambda x: x['last_committed_date'])

    out_data = []

    for row in repo_count_data:
        if row['branch_name']:
            if row['last_committed_date']:
                row['last_committed_date'] = lib.time.as_date(row['last_committed_date'])
            else:
                row['last_committed_date'] = None

            if start is None or row['last_committed_date'] >= start:
                out_data.append(row)

    return out_data


def repo_names(start=None):
    repos_summary = read(start)

    owner_name = repos_summary[0]['owner_name']

    return owner_name, [r['repo_name'] for r in repos_summary]


def test():
    rows = read()
    print(f"Total: {len(rows)}")
    print()
    preview = 3
    print(f"Latest {preview}")
    for row in rows[-1*preview:]:
        for k, v in row.items():
            print(f"{k:20}: {v}")
        print()

    print('repo_names')
    owner, names = repo_names()
    print(owner, len(names))

# If you care about volume
# Best to filter by date first and then sort results rather than sort afterwards
# If you just need more recent then repo_names with start is fine without filtering source data.


if __name__ == '__main__':
    test()
