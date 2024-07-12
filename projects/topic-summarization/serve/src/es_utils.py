"""Elasticsearch utils file."""

# Internal libraries
import re

# Standard Library
from datetime import datetime
from typing import List

# 3rd party libraries
from elasticsearch import Elasticsearch
from pydantic import SecretStr


def generate_crawler_indices(es_secret_value: SecretStr, num_months: int = 5) -> List:
    """Generate last 5 monthes indexes."""
    current_date = datetime.now()

    print("\n")
    print("\n")
    print("\n")
    print("ES SECRET VALUE :", es_secret_value)

    es = Elasticsearch(
        [
            f"https://crawler-prod:{es_secret_value}@search5-client.airpr.com"  # noqa: W505, E501
        ]
    )
    indices = es.indices.get_alias("*").keys()

    # Generate a list of the last num_months in "year.month" format
    recent_months = []
    year = current_date.year
    month = current_date.month
    for i in range(num_months):
        # Calculate the month and year
        recent_months.append(f"{year}.{month:02d}")

        # Adjust year and month if month is less than 1
        month -= 1
        if month < 1:
            month += 12
            year -= 1

    # Define the pattern to match the required format
    pattern = re.compile(r"crawler-\d{1,2}-\d{4}\.\d{2}")

    # Filter indices based on the pattern and recent months
    filtered_indices = [
        index
        for index in indices
        if pattern.match(index) and any(month in index for month in recent_months)
    ]
    filtered_indices.append("crawler")

    return filtered_indices
