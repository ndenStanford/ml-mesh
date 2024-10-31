"""Utility functions."""

# Standard Library
from collections import defaultdict


def impute_clean(times, column):
    """Impute missing values in a column based on linear interpolation between known values.

    Args:
        times (list): List of times for which values need to be imputed.
        column (list): List of tuples where each tuple contains a time and a value.

    Returns:
        list: List of imputed values for the given times.
    """
    acc = []
    times = list(times)
    while len(times) > 0:
        if len(column) == 0:
            acc.extend([None] * len(times))
            break
        t1, v1 = column[0]
        if len(column) == 1:
            acc.extend([v1 if t >= t1 else None for t in times])
            break
        t2, v2 = column[1]
        pre_interval_times = [t for t in times if t < t1]
        interval_times = [t for t in times if t1 <= t < t2]
        times = [t for t in times if t >= t2]
        interval_size = (t2 - t1).total_seconds()
        imputed = [
            int(
                (1 - (t2 - t).total_seconds() / interval_size) * v1
                + (t2 - t).total_seconds() / interval_size * v2
            )
            for t in interval_times
        ]
        acc.extend([None] * len(pre_interval_times) + imputed)
        column = column[1:]

    return acc


def impute_column(times, column):
    """Filter out None values from the column and impute missing values.

    Args:
        times (list): List of times for which values need to be imputed.
        column (list): List of tuples where each tuple contains a time and a value.

    Returns:
        list: List of imputed values for the given times.
    """
    return impute_clean(times, [(time, val) for time, val in column if val is not None])


def max_options(rows):
    """Return the maximum values from each column across multiple rows.

    Args:
        rows (list): List of rows, where each row is a list containing values for multiple columns.

    Returns:
        list: A list of maximum values for each column.
    """
    # Transpose the rows to get columns
    columns = zip(*rows)

    result = []
    for column in columns:
        # Filter out None values explicitly
        filtered = [value for value in column if value is not None]
        # If there are valid values, take the max; otherwise, keep None
        max_value = max(filtered) if filtered else None
        result.append(max_value)

    return result


def merge_duplicates(metadatas):
    """Merge duplicate rows by date, selecting the maximum value for each column.

    Args:
        metadatas (list): List of tuples, where each tuple contains a date and metadata for that date.

    Returns:
        list: A list of tuples with merged metadata for each unique date.
    """
    grouped = defaultdict(list)
    for date, meta in metadatas:
        grouped[date].append(meta)
    return sorted((date, max_options(rows)) for date, rows in grouped.items())


def impute_by_columns(times, metadatas):
    """Impute metadata by columns over the given time intervals.

    Args:
        times (list): List of time intervals for which metadata needs to be imputed.
        metadatas (list): List of metadata entries for each time interval.

    Returns:
        list: A list of imputed metadata for each time interval.
    """
    metadatas_new = merge_duplicates(metadatas)
    if all(len(x[1]) == 0 for x in metadatas_new):
        return [(time, []) for time in times]
    row_data = [[(date, val) for val in metadata] for date, metadata in metadatas_new]
    columns = list(zip(*row_data))
    imputed_columns = [impute_column(times, column) for column in columns]
    transposed_result = list(zip(*imputed_columns))
    return list(zip(times, transposed_result))


def get_relevance_percentile(relevance_map, profile_id, relevance):
    """Get the relevance percentile for a given profile ID and relevance value.

    Args:
        relevance_map (dict): A dictionary where keys are profile IDs (integers) and
                              values are sorted dictionaries (TreeMap equivalent) with
                              relevance values as keys and percentiles as values.
        profile_id (int): The ID of the profile for which relevance needs to be checked.
        relevance (float): The relevance value for which to find the closest percentile.

    Returns:
        float: The percentile value if found, otherwise 0.0.
    """
    if profile_id in relevance_map:
        tree_map = relevance_map[profile_id]
        closest_key = max((k for k in tree_map if k <= relevance), default=None)
        return tree_map[closest_key] if closest_key is not None else 0.0
    else:
        return 0.0


def snake_to_camel(snake_str):
    """Convert a snake_case string to camelCase.

    Args:
        snake_str (str): The input string in snake_case format.

    Returns:
        str: The converted string in camelCase format.
    """
    components = snake_str.split("_")
    camel_str = components[0] + "".join(x.title() for x in components[1:])
    return camel_str


def convert_df_columns_to_camel(df, excluded_columns=None):
    """Convert the snake_case column names of a DataFrame to camelCase.

    Args:
        df (pd.DataFrame): The input DataFrame with column names in snake_case.
        excluded_columns (list, optional): A list of columns to be excluded from conversion.

    Returns:
        pd.DataFrame: A DataFrame with column names converted to camelCase (except the excluded ones).
    """
    if excluded_columns is None:
        excluded_columns = []

    new_columns = []
    for col in df.columns:
        if col in excluded_columns:
            new_columns.append(col)
        else:
            new_columns.append(snake_to_camel(col))

    df.columns = new_columns
    return df
