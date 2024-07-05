"""Elasticsearch utils file."""

# Internal libraries
# 3rd party libraries
from datetime import datetime

# Standard Library
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
        while target_month <= 0:
            target_month += 12
            target_year -= 1

        month_str = f"{target_year}.{target_month:02d}"
        index = f"crawler-4-{month_str}"
        indices.append(index)
    indices.append("crawler")

    return indices
