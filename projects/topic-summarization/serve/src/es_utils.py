"""Elasticsearch utils file."""

# Internal libraries
# 3rd party libraries

# Standard Library
from datetime import datetime
from typing import List


def generate_crawler_indices(num_months: int = 5) -> List:
    """Generate last 5 monthes indexes."""
    current_date = datetime.now()
    indices = []

    for i in range(num_months):
        # Calculate the target month and year
        target_year = current_date.year
        target_month = current_date.month - i

        # Adjust the year and month if needed
        # while loop can be avoided if using dateutil. But will get issue in updating poetry.lock.
        # So keep this for now and will update in the future
        while target_month <= 0:
            target_month += 12
            target_year -= 1

        month_str = f"{target_year}.{target_month:02d}"
        month_str = f"{target_year}.{target_month:02d}"
        if month_str == "2024.06":
            index = f"crawler-5-{month_str}"
        else:
            index = f"crawler-4-{month_str}"
        indices.append(index)
    indices.append("crawler")

    return indices
