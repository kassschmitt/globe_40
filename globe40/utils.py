import math
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar


def extend_interval(
    start_date, end_date, percentage_to_change=0, days_either_end=0, year_shift=-2
):
    """
    Calculates a new end date if duration is increased by percentage_to_change and then
    Subtracts/adds days_either_end to start/end respectively. Returns adjusted start and
    end dates.

    Parameters:
    - start_date (str): The start date in 'YYYY-MM-DD' format.
    - end_date (str): The end date in 'YYYY-MM-DD' format.
    - percentage to change (int): the percentage change in duration.
    - days_either_end (int): number of days to pad the interval with at either end.

    Returns:
    - tuple: A tuple containing the adjusted start and end dates in 'YYYY-MM-DD' format.

    Raises:
    - ValueError: If the start_date is after the end_date.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Check if start_date is earlier than end_date
    if start > end:
        raise ValueError(
            "The end date must be greater than or equal to the start date."
        )
    # shift start and end years by year_shift
    start = start + relativedelta(years=year_shift)
    end = end + relativedelta(years=year_shift)

    duration = (end - start).days
    change_factor = 1.0 + (percentage_to_change / 100)
    if change_factor < 1:
        new_duration = math.floor(duration * change_factor)
    else:
        new_duration = math.ceil(duration * change_factor)
    new_end = start + timedelta(days=new_duration + days_either_end)
    new_start = start - timedelta(days=days_either_end)

    return (new_start.strftime("%Y-%m-%d"), new_end.strftime("%Y-%m-%d"))


def get_days_in_interval(start_date, end_date):
    """
    Returns a list of tuples representing the intervals of days between start_date and end_date.

    Parameters:
    - start_date (str): The start date in 'YYYY-MM-DD' format.
    - end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
    - list: A list of tuples, each representing a month in the form (year, month, list(range(start_day, end_day))).

    Raises:
    - ValueError: If the start_date is after the end_date.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Check if start_date is earlier than end_date
    if start > end:
        raise ValueError(
            "The end date must be greater than or equal to the start date."
        )

    result = []
    current = start

    while current <= end:
        year = current.year
        month = current.month
        start_day = current.day
        # Find the last day of the current month
        last_day_of_month = calendar.monthrange(year, month)[1]
        # If the current month extends beyond the end date, adjust the end day
        end_day = min(
            last_day_of_month,
            (
                end.day
                if current.year == end.year and current.month == end.month
                else last_day_of_month
            ),
        )

        result.append(
            (year, month, ["{}".format(i) for i in list(range(start_day, end_day + 1))])
        )

        # Move to the first day of the next month
        next_month = current.replace(day=28) + timedelta(
            days=4
        )  # this will always go to the next month
        current = next_month.replace(day=1)

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python script_name.py <start_date> <end_date>")
        print("Example: python script_name.py 2024-01-15 2024-03-05")
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]

    try:
        intervals = get_days_in_interval(start_date, end_date)
        print(intervals)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
