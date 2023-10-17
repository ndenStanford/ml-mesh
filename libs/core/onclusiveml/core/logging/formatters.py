"""Logging formatters."""

# Standard Library
import logging

# 3rd party libraries
import pydantic


class OnclusiveJSONLogRecord(pydantic.BaseModel):
    """Standard JSON log format for all onclusive python (ML) applications."""

    asctime: str
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
            asctime=record.asctime,
            levelname=record.levelname,
            name=record.name,
            pathName=record.pathname,
            filename=record.filename,
            funcName=record.funcName,
            lineno=record.lineno,
            message=formatted_message,
        )

        return formatted_record.json()
