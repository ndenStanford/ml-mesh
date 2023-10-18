"""Formatters test suite."""

# Standard Library
import logging

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


def test_onclusive_serving_json_default_formatter(monkeypatch):
    """Tests the OnclusiveServingJSONAccessFormatter `formatMessage` method."""
    # patch Formatter.formatTime with dummy time stamp
    def dummy_format_time(self, record, datefmt=None):
        return "dummy time stamp"

    monkeypatch.setattr(logging.Formatter, "formatTime", dummy_format_time)

    formatter = OnclusiveServingJSONDefaultFormatter(
        fmt=OnclusiveLogMessageFormat.SIMPLE.value
    )

    test_record = logging.LogRecord(
        name="test logger",
        level=10,
        pathname="",
        msg="test message",
        func="test function",
        lineno=1,
        exc_info=None,
        args=None,
    )
    formatted_message_actual = formatter.format(test_record)

    assert (
        formatted_message_actual
        == '{"asctime": "dummy time stamp", "levelname": "DEBUG", "name": "test logger", "filename": "", "funcName": "test function", "lineno": 1, "message": "dummy time stamp - DEBUG - test message"}'  # noqa: E501
    )  # noqa: E501


def test_onclusive_serving_json_access_formatter(monkeypatch):
    """Tests the OnclusiveServingJSONAccessFormatter `formatMessage` method."""
    # patch Formatter.formatTime with dummy time stamp
    def dummy_format_time(self, record, datefmt=None):
        return "dummy time stamp"

    monkeypatch.setattr(logging.Formatter, "formatTime", dummy_format_time)

    formatter = OnclusiveServingJSONAccessFormatter(
        fmt=OnclusiveLogMessageFormat.SIMPLE.value
    )

    test_record = logging.LogRecord(
        name="test logger",
        level=10,
        pathname="",
        msg='test message: %s - "%s %s HTTP/%s" %d',
        func="test function",
        lineno=1,
        args=("test.client.address", "TEST", "test_host://test/path", 1, 1),
        exc_info=None,
    )
    formatted_message_actual = formatter.format(test_record)

    assert (
        formatted_message_actual
        == '{"asctime": "dummy time stamp", "levelname": "DEBUG", "name": "test logger", "filename": "", "funcName": "test function", "lineno": 1, "message": "dummy time stamp - DEBUG - test message: test.client.address - \\"TEST test_host://test/path HTTP/1\\" 1", "client_addr": "test.client.address", "request_line": "\\u001b[1mTEST test_host://test/path HTTP/1\\u001b[0m", "status_code": 1}'  # noqa: E501
    )  # noqa: E501
