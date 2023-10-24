"""Formatters test suite."""

# Standard Library
import logging

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import (
    OnclusiveJSONFormatter,
    OnclusiveJSONLogRecord,
    OnclusiveLogMessageFormat,
)


@pytest.mark.parametrize("service", ["test-service", "onclusive-ml"])
def test_onclusive_json_log_record(service):
    """Tests the OnclusiveJSONLogRecord constructor with basic sample inputs."""
    OnclusiveJSONLogRecord(
        service=service,
        asctime="test asctime",
        levelname="test log level name",
        name="test logger name",
        filename="test file name",
        funcName="test function name",
        lineno=1,
        message="test log message",
    )


@pytest.mark.parametrize(
    "fmt, expected_formatted_message",
    [
        (
            OnclusiveLogMessageFormat.MESSAGE_ONLY.value,
            '{"service": "test-service", "asctime": null, "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "testing message formatting"}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.BASIC.value,
            '{"service": "test-service", "asctime": null, "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "INFO - testing message formatting"}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.SIMPLE.value,
            '{"service": "test-service", "asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "dummy time stamp - INFO - testing message formatting"}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.DETAILED.value,
            '{"service": "test-service", "asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "dummy time stamp - [INFO] - test logger - (testfile.py).test_function(1) - testing message formatting"}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.JSON.value,
            '{"service": "test-service", "asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "[test-service] - dummy time stamp - [INFO] - test logger - (testfile.py).test_function(1) - testing message formatting"}',  # noqa: E501
        ),
    ],
)
def test_onclusive_json_formatter_format(monkeypatch, fmt, expected_formatted_message):
    """Tests the OnclusiveJSONFormatter `format` method."""
    # patch Formatter.formatTime with dummy time stamp
    def dummy_format_time(self, record, datefmt=None):
        return "dummy time stamp"

    monkeypatch.setattr(logging.Formatter, "formatTime", dummy_format_time)

    formatter = OnclusiveJSONFormatter(service="test-service", fmt=fmt)

    test_record = logging.LogRecord(
        name="test logger",
        level=20,
        pathname="testfile.py",
        msg="testing message formatting",
        func="test_function",
        lineno=1,
        args=None,
        exc_info=None,
    )
    actual_formatted_message = formatter.format(test_record)

    assert actual_formatted_message == expected_formatted_message
