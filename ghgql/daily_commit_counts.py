#!/usr/bin/env python
"""
Daily commit counts report application.

Get commit contributions of a user by day over a few years, using `weekly` from
the API. The API response groups days by weeks, so this report flattens that
to one row for each day.

See the docs for sample output.
"""
import lib

QUERY_PATH = "queries/contributions/daily_commit_counts.gql"


def process_weeks(value):
    year_of_weeks = value["contributionCalendar"]["weeks"]

    out_days = {}
    for week in year_of_weeks:
        for day in week["contributionDays"]:
            date = day["date"]
            count = day["contributionCount"]
            out_days[date] = count

    return out_days


def process():
    resp_data = lib.query_by_filename(QUERY_PATH)

    user_years = resp_data["viewer"]
    # We don't actually care about the year keys, as the dates are in granular
    # data.
    contributions_by_year = [process_weeks(v) for v in user_years.values()]

    all_contributions = {}
    for year in contributions_by_year:
        all_contributions.update(**year)

    return all_contributions


def main():
    """
    Command-line entrypoint.
    """
    all_contributions = process()

    print("date,contributions")

    for date in sorted(all_contributions.keys()):
        count = all_contributions[date]
        print(f"{date},{count}")


if __name__ == "__main__":
    main()
