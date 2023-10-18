"""Formatters test suite."""

# Standard Library
import logging

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import OnclusiveLogMessageFormat
from onclusiveml.serving.rest.observability import (
    OnclusiveServingJSONAccessFormatter,
    OnclusiveServingJSONAccessLogRecord,
    OnclusiveServingJSONDefaultFormatter,
    OnclusiveServingJSONDefaultLogRecord,
)


def test_onclusive_serving_json_access_log_record():
    """Tests the OnclusiveServingJSONAccessLogRecord constructor with basic sample inputs."""
    OnclusiveServingJSONAccessLogRecord(
        asctime="test asctime",
        levelname="test log level name",
        name="test logger name",
        filename="test file name",
        funcName="test function name",
        lineno=1,
        message="test log message",
        client_addr="test client address",
        request_line="test request line",
        status_code=1,
    )


def test_onclusive_serving_json_default_log_record():
    """Tests the OnclusiveServingJSONDefaultLogRecord constructor with basic sample inputs."""
    OnclusiveServingJSONDefaultLogRecord(
        asctime="test asctime",
        levelname="test log level name",
        name="test logger name",
        filename="test file name",
        funcName="test function name",
        lineno=1,
        message="test log message",
        color_message="test colour message",
    )


@pytest.mark.parametrize(
    "fmt, expected_formatted_message",
    [
        (
            OnclusiveLogMessageFormat.MESSAGE_ONLY.value,
            '{"asctime": null, "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "testing message formatting", "color_message": null}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.BASIC.value,
            '{"asctime": null, "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "INFO - testing message formatting", "color_message": null}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.SIMPLE.value,
            '{"asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "dummy time stamp - INFO - testing message formatting", "color_message": null}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.DETAILED.value,
            '{"asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "dummy time stamp - [INFO] - test logger - (testfile.py).test_function(1) - testing message formatting", "color_message": null}',  # noqa: E501
        ),
    ],
)
def test_onclusive_serving_json_default_formatter_format(
    monkeypatch, fmt, expected_formatted_message
):
    """Tests the OnclusiveServingJSONDefaultFormatter `format` method."""
    # patch Formatter.formatTime with dummy time stamp
    def dummy_format_time(self, record, datefmt=None):
        return "dummy time stamp"

    monkeypatch.setattr(logging.Formatter, "formatTime", dummy_format_time)

    formatter = OnclusiveServingJSONDefaultFormatter(fmt=fmt)

    test_record = logging.LogRecord(
        name="test logger",
        level=20,
        pathname="testfile.py",
        msg="testing message formatting",
        func="test_function",
        lineno=1,
        exc_info=None,
        args=None,
    )
    actual_message_actual = formatter.format(test_record)

    assert actual_message_actual == expected_formatted_message


@pytest.mark.parametrize(
    "fmt, expected_formatted_message",
    [
        (
            OnclusiveLogMessageFormat.MESSAGE_ONLY.value,
            '{"asctime": null, "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "test message: test.client.address - \\"TEST test_host://test/path HTTP/1\\" 1", "client_addr": "test.client.address", "request_line": "\\u001b[1mTEST test_host://test/path HTTP/1\\u001b[0m", "status_code": 1}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.BASIC.value,
            '{"asctime": null, "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "INFO - test message: test.client.address - \\"TEST test_host://test/path HTTP/1\\" 1", "client_addr": "test.client.address", "request_line": "\\u001b[1mTEST test_host://test/path HTTP/1\\u001b[0m", "status_code": 1}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.SIMPLE.value,
            '{"asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "dummy time stamp - INFO - test message: test.client.address - \\"TEST test_host://test/path HTTP/1\\" 1", "client_addr": "test.client.address", "request_line": "\\u001b[1mTEST test_host://test/path HTTP/1\\u001b[0m", "status_code": 1}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.DETAILED.value,
            '{"asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "dummy time stamp - [INFO] - test logger - (testfile.py).test_function(1) - test message: test.client.address - \\"TEST test_host://test/path HTTP/1\\" 1", "client_addr": "test.client.address", "request_line": "\\u001b[1mTEST test_host://test/path HTTP/1\\u001b[0m", "status_code": 1}',  # noqa: E501
        ),
    ],
)
def test_onclusive_serving_json_access_formatter_format(
    monkeypatch, fmt, expected_formatted_message
):
    """Tests the OnclusiveServingJSONAccessFormatter `format` method."""
    # patch Formatter.formatTime with dummy time stamp
    def dummy_format_time(self, record, datefmt=None):
        return "dummy time stamp"

    monkeypatch.setattr(logging.Formatter, "formatTime", dummy_format_time)

    formatter = OnclusiveServingJSONAccessFormatter(fmt=fmt)

    test_record = logging.LogRecord(
        name="test logger",
        level=20,
        pathname="testfile.py",
        msg='test message: %s - "%s %s HTTP/%s" %d',
        func="test_function",
        lineno=1,
        args=("test.client.address", "TEST", "test_host://test/path", 1, 1),
        exc_info=None,
    )
    actual_formatted_message = formatter.format(test_record)

    assert actual_formatted_message == expected_formatted_message
