"""
Read counts script.

Read the repos and counts CSV and return date
"""
import datetime

import lib

DATE_FORMAT = '%Y-%m-%d'


def read(start=None):
    """
    Read CSV, order by date, parse date then return.

    If start is set as 'YYYY-MM-DD', then filter results to only that date or
    after.
    """
    if start:
        start_date = datetime.datetime.strptime(start, DATE_FORMAT).date()
    else:
        start_date = None

    repo_count_data = lib.read_csv(lib.COUNTS_CSV_PATH)

    repo_count_data.sort(key=lambda x: x['last_committed_date'])

    out_data = []

    for row in repo_count_data:
        date = row['last_committed_date']
        if date:
            row['last_committed_date'] = datetime.datetime.strptime(
                date, DATE_FORMAT
            ).date()
        else:
            row['last_committed_date'] = None

        if start_date is None or row['last_committed_date'] >= start:
            out_data.append(row)

    return out_data


def test():
    rows = read()
    print(len(rows))
    for row in rows[-3:]:
        for k, v in row.items():
            print(f"{k:20}: {v}")
        print()


if __name__ == '__main__':
    test()
