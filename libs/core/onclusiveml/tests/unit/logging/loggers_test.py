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
    get_default_logger_from_env,
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
    """Tests the basic functionality of the get_default_logger method using a custom handler."""
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
    """Tests the basic functionality of the get_default_logger method using the default handler."""
    # patch sys.stdout with local buffer
    buffer = StringIO()
    monkeypatch.setattr(sys, "stdout", buffer)

    # patch Logger.findCaller with dummy file name and line number
    def dummy_find_caller(self, stack_info=False, stacklevel=1):
        return ("testfile.py", 1, "test_function", None)

    monkeypatch.setattr(logging.Logger, "findCaller", dummy_find_caller)

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
    expected_log_entry = '{"asctime": null, "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "testing logging format"}\n'  # noqa: E501
    assert actual_log_entry == expected_log_entry


def test_get_default_logger_from_env_message_format(monkeypatch):
    """Tests the basic functionality of the get_default_logger_from_env method."""
    # patch sys.stdout with local buffer
    buffer = StringIO()
    monkeypatch.setattr(sys, "stdout", buffer)

    # patch Formatter.formatTime with dummy time stamp
    def dummy_format_time(self, record, datefmt=None):
        return "dummy time stamp"

    monkeypatch.setattr(logging.Formatter, "formatTime", dummy_format_time)

    # patch Logger.findCaller with dummy file name and line number
    def dummy_find_caller(self, stack_info=False, stacklevel=1):
        return ("testfile.py", 1, "test_function", None)

    monkeypatch.setattr(logging.Logger, "findCaller", dummy_find_caller)

    # use
    logger = get_default_logger_from_env("test logger")

    msg = "testing logging format"
    logger.debug(msg)

    actual_log_entry = buffer.getvalue()
    expected_log_entry = '{"asctime": "dummy time stamp", "levelname": "DEBUG", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "dummy time stamp - DEBUG - testing logging format"}\n'  # noqa: E501
    assert actual_log_entry == expected_log_entry
