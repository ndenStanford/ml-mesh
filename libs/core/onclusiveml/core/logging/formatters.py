"""Logging formatters."""

# Standard Library
import logging

# 3rd party libraries
import pydantic


class OnclusiveJSONLogRecord(pydantic.BaseModel):
    """Standard JSON log format for all onclusive python (ML) applications."""

    user: str
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
        super().formatMessage(record)

        log_record = OnclusiveJSONLogRecord(
            asctime=record.asctime,
            levelname=record.levelname,
            name=record.name,
            pathName=record.pathname,
            funcName=record.funcName,
            lineNumber=record.lineno,
            message=record.message,
        )

        return log_record.json(log_record)
