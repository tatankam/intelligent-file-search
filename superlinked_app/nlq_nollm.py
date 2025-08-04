import datetime
import re
from typing import Dict, Any
from dateutil.relativedelta import relativedelta
from superlinked import framework as sl
from superlinked_app.nlq import get_cat_options


# Load file type options for param
cat_options = get_cat_options()
filetype_options = cat_options.get("FileType", [])


# Declare the parameters here, so they can be imported elsewhere
filetype_include_any_param = sl.Param(
    "filetype_include_any",
    description="File can match any of these file types",
    options=filetype_options,
)


min_creation_date_param = sl.Param(
    "min_creation_date",
    description="Minimum creation date (unix timestamp in seconds)",
)


max_creation_date_param = sl.Param(
    "max_creation_date",
    description="Maximum creation date (unix timestamp in seconds)",
)


# Define valid file types for simple parsing
VALID_FILETYPES = set(filetype_options) if filetype_options else {"pdf", "docx", "txt", "md"}


def unix_timestamp(dt: datetime.datetime) -> int:
    """Convert datetime to unix timestamp in milliseconds."""
    return int(dt.timestamp() * 1000)


def parse_simple_nollm(query: str) -> Dict[str, Any]:
    """
    Parse simple natural query to structured parameters matching the declared sl.Params.

    Returns dict with keys:
    - filetype_include_any: list[str] or None
    - min_creation_date: int (unix ms) or None
    - max_creation_date: int (unix ms) or None
    """
    query = query.lower().strip()
    params = {
        "filetype_include_any": None,
        "min_creation_date": None,
        "max_creation_date": None,
    }

    # Extract file types mentioned
    words = query.split()
    filetypes = [w for w in words if w in VALID_FILETYPES]
    if filetypes:
        params["filetype_include_any"] = filetypes

    now = datetime.datetime.now()
    min_date = None
    max_date = None

    # Check for "last N units" e.g. "last 3 years", "last 6 months", "last 10 days"
    match = re.search(r"last (\d+) (day|week|month|year)s?", query)
    if match:
        number = int(match.group(1))
        unit = match.group(2)

        if unit == "day":
            min_date = now - datetime.timedelta(days=number)
        elif unit == "week":
            min_date = now - datetime.timedelta(weeks=number)
        elif unit == "month":
            min_date = now - relativedelta(months=number)
        elif unit == "year":
            min_date = now - relativedelta(years=number)

        max_date = now
        # Normalize min_date and max_date to start/end of day
        min_date = datetime.datetime(min_date.year, min_date.month, min_date.day)
        max_date = datetime.datetime(max_date.year, max_date.month, max_date.day, 23, 59, 59)

    elif "last week" in query:
        weekday = now.weekday()
        last_monday = now - datetime.timedelta(days=weekday + 7)
        last_sunday = last_monday + datetime.timedelta(days=6)
        min_date = datetime.datetime(last_monday.year, last_monday.month, last_monday.day)
        max_date = datetime.datetime(last_sunday.year, last_sunday.month, last_sunday.day, 23, 59, 59)

    elif "yesterday" in query:
        yesterday = now - datetime.timedelta(days=1)
        min_date = datetime.datetime(yesterday.year, yesterday.month, yesterday.day)
        max_date = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)

    elif "today" in query:
        min_date = datetime.datetime(now.year, now.month, now.day)
        max_date = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)

    elif "last month" in query:
        first_day_this_month = datetime.datetime(now.year, now.month, 1)
        last_month_end = first_day_this_month - datetime.timedelta(days=1)
        last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
        min_date = last_month_start
        max_date = datetime.datetime(last_month_end.year, last_month_end.month, last_month_end.day, 23, 59, 59)

    if min_date:
        params["min_creation_date"] = unix_timestamp(min_date)
    if max_date:
        params["max_creation_date"] = unix_timestamp(max_date)

    return params
