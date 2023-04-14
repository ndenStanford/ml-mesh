"""Logger."""

# Standard Library
import logging

# Internal libraries
from onclusiveml.core.logging.constants import (
    DEFAULT_LOGGING_HANDLER,
    LogFormat,
)


def get_default_logger(
    name: str,
    handler: logging.Handler = DEFAULT_LOGGING_HANDLER,
    fmt: LogFormat = LogFormat.SIMPLE.value,
    level: int = logging.DEBUG,
) -> logging.Logger:
    """Instantiates default logger."""
    logger = logging.getLogger(name)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger
