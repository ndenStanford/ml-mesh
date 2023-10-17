"""Logging formatters."""

# Standard Library
import logging
from typing import Optional

# 3rd party libraries
import pydantic


class OnclusiveJSONLogRecord(pydantic.BaseModel):
    """Standard JSON log format for all onclusive python (ML) applications."""

    # The asctime attribute is dynamic and depends on the fmt, so needs to be optional if users
    # decide to use a fmt that doesnt support the asctime attribute creation (e.g.
    # OnclusiveLogMessageFormat.MESSAGE_ONLY.value and OnclusiveLogMessageFormat.BASIC.value).
    # Source: https://github.com/python/cpython/blob/232465204edb070751f4794c67dd31cd9b7c8c53/...
    # ...Lib/logging/__init__.py#L704
    asctime: Optional[str] = None
    levelname: str
    name: str
    filename: str
    funcName: str
    lineno: int
    message: str


class OnclusiveJSONFormatter(logging.Formatter):
    """Standard JSON log record formatter for all onclusive python (ML) applications."""

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Converts a LogRecord instance to JSON using the OnclusiveJSONLogRecord data model."""
        formatted_message = super().formatMessage(record)

        formatted_record = OnclusiveJSONLogRecord(
            asctime=getattr(record, "asctime", None),
            levelname=record.levelname,
            name=record.name,
            pathName=record.pathname,
            filename=record.filename,
            funcName=record.funcName,
            lineno=record.lineno,
            message=formatted_message,
        )

        return formatted_record.json()
