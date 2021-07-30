#!/usr/bin/env python
"""
Weekly report application.

Get contributions of a user by day, using `weekly` from the API.

e.g.
    2019-03-27 7
    2019-03-28 4
    2019-03-29 6
    2019-03-30 8
    2019-03-31 0
    ...
    2021-03-24 17
    2021-03-25 60
    2021-03-26 6
    2021-03-27 41
    2021-03-28 74
    2021-03-29 30
    2021-03-30 69
"""
import lib

QUERY_PATH = "queries/contributions/weekly.gql"


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
