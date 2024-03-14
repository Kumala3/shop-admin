import pytz


def format_created_at(model, name):
    """
    Formats the created_at attribute of a model to a specific date and time format.

    Args:
        model: The model object.
        name: The name of the attribute representing the created_at date.

    Returns:
        str: The formatted date and time string in the format "%Y-%m-%d %H:%M:%S".
    """
    utc_date = getattr(model, name)
    if utc_date is None:
        return ""

    # Convert UTC Datetime to GMT+3
    timezone = pytz.timezone("Europe/Moscow")
    local_date = utc_date.replace(tzinfo=pytz.utc).astimezone(timezone)
    formatted_date = local_date.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date
