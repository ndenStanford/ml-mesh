"""Timing decorator."""

# Wrapper that checks time to run function, then log it
# make so can deal with unkonwn amount of parameters

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger

# Standard Library
from typing import Any, Callable, List, Optional
import datetime

logger = get_default_logger(__name__)

def timing_decorator(func) -> Callable:
    def wrapper(*args, **kwargs) -> None:
        start_time = datetime.datetime.utcnow()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.utcnow()
        logger.info('Total Time in milliseconds = {}'.format((end_time - start_time).total_seconds()*1000))
        return result
    return wrapper
