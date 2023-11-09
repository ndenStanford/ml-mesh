"""Formatters."""

# Standard Library
import http
import logging
from copy import copy

# Internal libraries
from onclusiveml.core.logging.formatters import (
    OnclusiveJSONFormatter,
    OnclusiveLogRecord,
)


class OnclusiveServingJSONAccessLogRecord(OnclusiveLogRecord):
    """Data model for log records generated by uvicorn.logging.AccessFormatter."""

    client_addr: str
    request_line: str
    status_code: int
    status_phrase: str


class OnclusiveServingJSONAccessFormatter(OnclusiveJSONFormatter):
    """Essentially extends a non-coloured uvicorn.logging.AccessFormatter with json formatting."""

    log_record_data_model = OnclusiveServingJSONAccessLogRecord

    @staticmethod
    def get_status_phrase(status_code: int) -> str:
        """Retrieves the pass/fail phrase associated with the given status code.

        Args:
            status_code (int): An HTTP status response code.

        Returns:
            str: A phrase describing the status code.
        """
        return http.HTTPStatus(status_code).phrase

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Adds request related data to log record attribute, then converts to JSON.

        Eseentially extends a non-coloured uvicorn.logging.AccessFormatter.formatMessage with a json
        conversion postprocessing step.

        Source: https://github.com/encode/uvicorn/blob/40b99b8436c0c261e3a85d10e291424072946292/...
            ...uvicorn/logging.py#L97
        """
        record_copy = copy(record)
        # /uvicorn.logging.AccessFormatter.formatMessage
        (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
        ) = record_copy.args  # type: ignore[misc]
        status_code = int(status_code)  # type: ignore[arg-type]
        status_phrase = self.get_status_phrase(status_code)
        request_line = "%s %s HTTP/%s" % (method, full_path, http_version)
        record_copy.__dict__.update(
            {
                "client_addr": client_addr,
                "request_line": request_line,
                "status_code": status_code,
                "status_phrase": status_phrase,
            }
        )
        # uvicorn.logging.AccessFormatter.formatMessage/

        formatted_record = super().formatMessage(record_copy)

        return formatted_record