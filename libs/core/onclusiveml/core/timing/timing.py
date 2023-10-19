"""Timing decorator."""

# Standard Library
import datetime
from typing import Any, Callable

# Internal libraries
from onclusiveml.core.logging import INFO, get_default_logger


logger = get_default_logger(__name__, INFO)


def timing_decorator(func: Callable) -> Callable:
    """A decorator function that measures execution time of a given function.

    Args:
        func (Callable): The function to be timed

    Example:
        >>> @timing_decorator
        >>> def my_function():
        >>>     ...

        >>> my_function() # execution time will be logged
    """

    def wrapper(*args: Any, **kwargs: Any) -> None:
        start_time = datetime.datetime.utcnow()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.utcnow()
        logger.info(
            "Total Time in milliseconds = {}".format(
                (end_time - start_time).total_seconds() * 1000
            )
        )
        return result

    return wrapper
