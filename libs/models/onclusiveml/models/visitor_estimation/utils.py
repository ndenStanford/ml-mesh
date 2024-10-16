"""Utility functions."""

# Standard Library
from collections import defaultdict


def imprec(intervaltimes, metadatawindows, metadata_old):
    """Impute metadata for missing intervals based on surrounding metadata windows.

    Args:
        intervaltimes (list): List of time intervals where metadata needs to be imputed.
        metadatawindows (list): List of tuples, where each tuple contains two metadata windows.
        metadata_old (list): Metadata to use when no new metadata is available.

    Returns:
        list: List of tuples containing the time and the imputed metadata.
    """
    acc = []
    while intervaltimes:
        if not metadatawindows:
            acc += [(t, metadata_old) for t in intervaltimes]
            break
        (tmd1, md1), (tmd2, md2) = metadatawindows[0]
        interval_times, intervaltimes = [t for t in intervaltimes if t < tmd2], [
            t for t in intervaltimes if t >= tmd2
        ]
        interval_size = (tmd2 - tmd1).total_seconds()
        imputed = [
            (time, [int(prop1 * a + prop2 * b) for a, b in zip(md1, md2)])
            for time in interval_times
            for prop1, prop2 in [
                (
                    1 - (tmd2 - time).total_seconds() / interval_size,
                    (tmd2 - time).total_seconds() / interval_size,
                )
            ]
        ]
        acc += imputed
        metadatawindows = metadatawindows[1:]
    return acc


def maxOptions(rows):
    """Return the maximum values from each column across multiple rows.

    Args:
        rows (list): List of rows, where each row is a list containing values for multiple columns.

    Returns:
        list: A list of maximum values for each column.
    """
    return [max(filter(None, col), default=None) for col in zip(*[r[1] for r in rows])]


def mergeDuplicates(metadatas):
    """Merge duplicate rows by date, selecting the maximum value for each column.

    Args:
        metadatas (list): List of tuples, where each tuple contains a date and metadata for that date.

    Returns:
        list: A list of tuples with merged metadata for each unique date.
    """
    grouped = defaultdict(list)
    for date, meta in metadatas:
        grouped[date].append(meta)
    return sorted((date, maxOptions(rows)) for date, rows in grouped.items())


def imputeByColumns(times, metadatas):
    """Impute metadata by columns over the given time intervals.

    Args:
        times (list): List of time intervals for which metadata needs to be imputed.
        metadatas (list): List of metadata entries for each time interval.

    Returns:
        list: A list of imputed metadata for each time interval.
    """
    metadatas_new = mergeDuplicates(metadatas)
    if all(len(x[1]) == 0 for x in metadatas_new):
        return [(time, []) for time in times]
    rowData = [[(date, val) for val in metadata] for date, metadata in metadatas_new]
    columns = list(zip(*rowData))
    return list(
        zip(times, map(list, zip(*[imprec(times, column, None) for column in columns])))
    )
