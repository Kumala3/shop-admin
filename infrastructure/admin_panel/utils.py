import pytz


def format_created_at(model, name):
    utc_date = getattr(model, name)
    if utc_date is None:
        return ""

    # Convert UTC Datetime to GMT+3
    timezone = pytz.timezone("Europe/Moscow")
    local_date = utc_date.replace(tzinfo=pytz.utc).astimezone(timezone)
    formatted_date = local_date.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date
