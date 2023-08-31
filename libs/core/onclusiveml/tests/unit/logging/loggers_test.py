"""Logger test."""

# Standard Library
import logging
from io import StringIO

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger


def test_default_logger_init():
    """Test default logger init."""
    logger = get_default_logger(
        "pytest", fmt=LogFormat.SIMPLE.value, level=logging.INFO
    )
    assert not logger.disabled


def test_default_logger():
    """Test default logger setup."""
    buffer = StringIO()
    logger = get_default_logger(
        "pytest",
        logging.StreamHandler(buffer),
        LogFormat.MESSAGE_ONLY.value,
        level=logging.INFO,
    )
    msg = "testing logging format"
    logger.info(msg)
    log = buffer.getvalue()
    assert log == f"{msg}\n"


@pytest.mark.parametrize(
    "level", [logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL]
)
def test_logging_level(level):
    """Test logging level."""
    logger = get_default_logger("pytest", fmt=LogFormat.SIMPLE.value, level=level)
    assert logger.isEnabledFor(level)
