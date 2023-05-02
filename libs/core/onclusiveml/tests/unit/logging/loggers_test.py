"""Logger test."""

# Standard Library
import logging
from io import StringIO

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger


def default_logger_test():
    """Test default logger setup."""
    buffer = StringIO(newline="")
    logger = get_default_logger(
        "pytest", logging.StreamHandler(buffer), LogFormat.MESSAGE_ONLY.value
    )
    msg = "testing logging format"
    logger.info(msg)
    log = buffer.getvalue()

    assert log == f"{msg}\n"
