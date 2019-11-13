import lib


QUERY_PATH = 'queries/contributions/weekly.gql'


def process_weeks(value):
    year_of_weeks = value['contributionCalendar']['weeks']

    out_days = {}
    for week in year_of_weeks:
        for day in week['contributionDays']:
            date = day['date']
            count = day['contributionCount']
            out_days[date] = count

    return out_days


def process():
    resp_data = lib.query_by_filename(QUERY_PATH)

    user_years = resp_data['viewer']
    # We don't actually care about the year keys, as the dates are in granualar data.
    contributions_by_year = [process_weeks(v) for v in user_years.values()]
    all_contributions = {}
    for year in contributions_by_year:
        all_contributions.update(**year)

    return all_contributions


def main():
    all_contributions = process()
    for k in sorted(all_contributions):
        print(k, all_contributions[k])


if __name__ == '__main__':
    main()
