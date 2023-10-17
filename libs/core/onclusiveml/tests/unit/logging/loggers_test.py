"""Logger test."""

# Standard Library
import logging
import sys
from io import StringIO

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import (
    OnclusiveLogMessageFormat,
    get_default_logger,
)
from onclusiveml.core.logging.constants import VALID_LOG_LEVELS


@pytest.mark.parametrize("level", VALID_LOG_LEVELS)
@pytest.mark.parametrize("fmt_level", OnclusiveLogMessageFormat.list(names=True))
@pytest.mark.parametrize("json_format", [True, False])
def test_get_default_logger(level, fmt_level, json_format):
    """Tests the get_default_logger method with all valid input configurations."""
    logger = get_default_logger("pytest", level, fmt_level, json_format)

    assert len(logger.handlers) == 1
    assert not logger.disabled
    assert logger.isEnabledFor(level)


def test_get_default_logger_message_format_with_custom_handler():
    """Test default logger setup."""
    buffer = StringIO()
    logger = get_default_logger(
        "test logger",
        level=logging.INFO,
        fmt_level=OnclusiveLogMessageFormat.MESSAGE_ONLY.name,
        handler=logging.StreamHandler(buffer),
        json_format=True,
    )
    msg = "testing logging format"
    logger.info(msg)

    actual_log_entry = buffer.getvalue()
    expected_log_entry = f"{msg}\n"
    assert actual_log_entry == expected_log_entry


def test_get_default_logger_message_format_with_default_handler(monkeypatch):
    """Test default logger setup."""
    # patch sys.stdout with local buffer
    buffer = StringIO()
    monkeypatch.setattr(sys, "stdout", buffer)
    # use
    logger = get_default_logger(
        "test logger",
        level=logging.INFO,
        fmt_level=OnclusiveLogMessageFormat.MESSAGE_ONLY.name,
        json_format=True,
    )

    msg = "testing logging format"
    logger.info(msg)

    actual_log_entry = buffer.getvalue()
    expected_log_entry = '{"asctime": null, "levelname": "INFO", "name": "test logger", "filename": "loggers_test.py", "funcName": "test_get_default_logger_message_format_with_default_handler", "lineno": 65, "message": "testing logging format"}\n'  # noqa: E501
    assert actual_log_entry == expected_log_entry
