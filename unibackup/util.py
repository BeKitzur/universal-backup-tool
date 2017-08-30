import datetime


def get_date(date_format="%Y%m%dT%H%M%SZ"):
    date = datetime.datetime.now(datetime.timezone.utc)
    return date.strftime(date_format)
