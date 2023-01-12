import datetime


def find_date_range(dates: list):
    days = list(map(lambda x: [datetime.datetime.strptime(x[0].strftime('%Y-%m-%d'), '%Y-%m-%d')], dates.copy()))
    start = int(min(days)[0].strftime('%d'))
    end = int(max(days)[0].strftime('%d'))
    return start, end


def filter_dates(date_dict: dict):
    pass
