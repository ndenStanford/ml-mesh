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
)
from onclusiveml.serving.rest.serve.constants import (
    OnclusiveServingLogMessageFormat,
)


def test_onclusive_serving_json_access_log_record():
    """Tests the OnclusiveServingJSONAccessLogRecord constructor with basic sample inputs."""
    OnclusiveServingJSONAccessLogRecord(
        service="test-service",
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
        status_phrase="ok",
    )


@pytest.mark.parametrize(
    "fmt, expected_formatted_message",
    [
        (
            OnclusiveServingLogMessageFormat.ACCESS_JSON.value,
            '{"service": "test-service", "asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "test-service | dummy time stamp - [INFO] - test.client.address - \\"TEST test_host://test/path HTTP/1\\" 200 OK", "client_addr": "test.client.address", "request_line": "TEST test_host://test/path HTTP/1", "status_code": 200, "status_phrase": "OK"}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.SIMPLE.value,
            '{"service": "test-service", "asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "dummy time stamp - INFO - test message: test.client.address - \\"TEST test_host://test/path HTTP/1\\" 200", "client_addr": "test.client.address", "request_line": "TEST test_host://test/path HTTP/1", "status_code": 200, "status_phrase": "OK"}',  # noqa: E501
        ),
        (
            OnclusiveLogMessageFormat.DETAILED.value,
            '{"service": "test-service", "asctime": "dummy time stamp", "levelname": "INFO", "name": "test logger", "filename": "testfile.py", "funcName": "test_function", "lineno": 1, "message": "dummy time stamp - [INFO] - test logger - (testfile.py).test_function(1) - test message: test.client.address - \\"TEST test_host://test/path HTTP/1\\" 200", "client_addr": "test.client.address", "request_line": "TEST test_host://test/path HTTP/1", "status_code": 200, "status_phrase": "OK"}',  # noqa: E501
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

    formatter = OnclusiveServingJSONAccessFormatter(service="test-service", fmt=fmt)

    test_record = logging.LogRecord(
        name="test logger",
        level=20,
        pathname="testfile.py",
        msg='test message: %s - "%s %s HTTP/%s" %d',
        func="test_function",
        lineno=1,
        args=("test.client.address", "TEST", "test_host://test/path", 1, 200),
        exc_info=None,
    )
    actual_formatted_message = formatter.format(test_record)

    assert actual_formatted_message == expected_formatted_message
