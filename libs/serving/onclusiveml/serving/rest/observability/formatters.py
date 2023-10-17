"""Formatters."""

# Standard Library
import logging
from copy import copy

# 3rd party libraries
import click
from uvicorn.logging import AccessFormatter, DefaultFormatter

# Internal libraries
from onclusiveml.core.logging.formatters import (
    OnclusiveJSONFormatter,
    OnclusiveJSONLogRecord,
)


class OnclusiveServingJSONAccessLogRecord(OnclusiveJSONLogRecord):
    """Data model for log records generated by uvicorn.logging.AccessFormatter."""

    client_addr: str
    request_line: str
    status_code: int


class OnclusiveServingJSONDefaultLogRecord(OnclusiveJSONLogRecord):
    """Data model for log records generated by uvicorn.logging.DefaultFormatter."""

    color_message: str


class OnclusiveServingJSONAccessFormatter(AccessFormatter, OnclusiveJSONFormatter):
    """Extends uvicorn.logging.AccessFormatter with json formatting."""

    log_record_data_model = OnclusiveServingJSONAccessLogRecord

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Extends uvicorn.logging.AccessFormatter.formatMessage with json formatting step.

        Source: https://github.com/encode/uvicorn/blob/40b99b8436c0c261e3a85d10e291424072946292/...
            ...uvicorn/logging.py#L97
        """
        record_copy = copy(record)
        (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
        ) = record_copy.args  # type: ignore[misc]
        status_code = self.get_status_code(int(status_code))  # type: ignore[arg-type]
        request_line = "%s %s HTTP/%s" % (method, full_path, http_version)
        if self.use_colors:
            request_line = click.style(request_line, bold=True)
        record_copy.__dict__.update(
            {
                "client_addr": client_addr,
                "request_line": request_line,
                "status_code": status_code,
            }
        )

        formatted_record = self._jsonify_record(record)

        return formatted_record


class OnclusiveServingJSONDefaultFormatter(DefaultFormatter, OnclusiveJSONFormatter):
    """Extends uvicorn.logging.DefaultFormatter with json formatting."""

    log_record_data_model = OnclusiveServingJSONDefaultLogRecord

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Extends uvicorn.logging.DefaultFormatter.formatMessage with json formatting step.

        Source: https://github.com/encode/uvicorn/blob/40b99b8436c0c261e3a85d10e291424072946292/...
            ...uvicorn/logging.py#L55
        """
        record_copy = copy(record)
        levelname = record_copy.levelname
        if self.use_colors:
            levelname = self.color_level_name(levelname, record_copy.levelno)
            if "color_message" in record_copy.__dict__:
                record_copy.msg = record_copy.__dict__["color_message"]
                record_copy.__dict__["message"] = record_copy.getMessage()

        record_copy_json = self._jsonify_record(record_copy)

        return record_copy_json
