"""Formatters test suite."""

# Standard Library
from logging import LogRecord

# Internal libraries
from onclusiveml.core.logging import (
    OnclusiveJSONFormatter,
    OnclusiveJSONLogRecord,
    OnclusiveLogMessageFormat,
)


def test_onclusive_json_log_record():
    """Tests the OnclusiveJSONLogRecord constructor with basic sample inputs."""
    OnclusiveJSONLogRecord(
        asctime="test asctime",
        levelname="test log level name",
        name="test logger name",
        filename="test file name",
        funcName="test function name",
        lineno=1,
        message="test log message",
    )


def test_onclusive_json_formatter_format_message():
    """Tests the OnclusiveJSONFormatter `formatMessage` method."""
    formatter = OnclusiveJSONFormatter(fmt=OnclusiveLogMessageFormat.MESSAGE_ONLY.value)

    test_record = LogRecord(
        name="test logger",
        level=10,
        pathname="",
        msg="test message",
        func="test_onclusive_json_log_record",
        lineno=1,
        args=None,
        exc_info=None,
    )
    formatted_message_actual = formatter.format(test_record)

    assert (
        formatted_message_actual
        == '{"asctime": null, "levelname": "DEBUG", "name": "test logger", "filename": "", "funcName": "test_onclusive_json_log_record", "lineno": 1, "message": "test message"}'  # noqa: E501
    )  # noqa: E501
