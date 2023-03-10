"""Logging."""

import logging

from onclusiveml.core.constants import LogFormat, DEFAULT_LOGGING_HANDLER


def get_default_logger(
    name: str,
    handler: logging.Handler = DEFAULT_LOGGING_HANDLER,
    fmt: LogFormat = LogFormat.SIMPLE.value,
    level: int = logging.DEBUG,
) -> str:
    """Instantiates default logger."""
    logger = logging.getLogger(name)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger
