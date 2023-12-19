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
    logger = get_default_logger(
        service="test-service",
        name="pytest",
        level=level,
        fmt_level=fmt_level,
        json_format=json_format,
    )

    assert len(logger.handlers) == 1
    assert not logger.disabled
    assert logger.isEnabledFor(level)


def test_get_default_logger_message_format_with_custom_handler():
    """Tests the basic functionality of the get_default_logger method using a custom handler."""
    buffer = StringIO()
    logger = get_default_logger(
        service="test-service",
        name="test logger",
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


@pytest.mark.parametrize(
    "fmt_level, json_format, expected_log_entry",
    [
        (
            OnclusiveLogMessageFormat.MESSAGE_ONLY.name,
            False,
            "testing logging format\n",
        ),
        (
            OnclusiveLogMessageFormat.BASIC.name,
            False,
            "INFO - testing logging format\n",
        ),
        (
            OnclusiveLogMessageFormat.SIMPLE.name,
            False,
            "dummy time stamp - INFO - testing logging format\n",
        ),
        (
            OnclusiveLogMessageFormat.DETAILED.name,
            False,
            "dummy time stamp - [INFO] - test logger - (testfile.py).test_function(1) - testing logging format\n",  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.DEFAULT.name,
            False,
            "test logger - (testfile.py).test_function(1) - testing logging format\n",  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.MESSAGE_ONLY.name,
            True,
            '{"service": "test-service", "asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "testing logging format"}\n',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.BASIC.name,
            True,
            '{"service": "test-service", "asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "INFO - testing logging format"}\n',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.SIMPLE.name,
            True,
            '{"service": "test-service", "asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "dummy time stamp - INFO - testing logging format"}\n',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.DETAILED.name,
            True,
            '{"service": "test-service", "asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "dummy time stamp - [INFO] - test logger - (testfile.py).test_function(1) - testing logging format"}\n',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.DEFAULT.name,
            True,
            '{"service": "test-service", "asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "test logger - (testfile.py).test_function(1) - testing logging format"}\n',  # noqa: E501
        ),
    ],
)
def test_get_default_logger_message_format_with_default_json_handler(
    monkeypatch, fmt_level, json_format, expected_log_entry
):
    """Tests the basic functionality of the get_default_logger method using the default handler."""
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
    logger = get_default_logger(
        service="test-service",
        name="test logger",
        level=logging.INFO,
        fmt_level=fmt_level,
        json_format=json_format,
    )

    msg = "testing logging format"
    logger.info(msg)

    actual_log_entry = buffer.getvalue()
    assert actual_log_entry == expected_log_entry
