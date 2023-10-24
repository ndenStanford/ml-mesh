"""Logging formatters."""

# Standard Library
import logging
from copy import copy
from typing import Literal, Optional

# 3rd party libraries
import pydantic

# Internal libraries
from onclusiveml.core.logging.constants import OnclusiveService


class OnclusiveJSONLogRecord(pydantic.BaseModel):
    """Standard JSON log format for all onclusive python (ML) applications."""

    # The asctime attribute is dynamic and depends on the fmt, so needs to be optional if users
    # decide to use a fmt that doesnt support the asctime attribute creation (e.g.
    # OnclusiveLogMessageFormat.MESSAGE_ONLY.value and OnclusiveLogMessageFormat.BASIC.value).
    # Source: https://github.com/python/cpython/blob/232465204edb070751f4794c67dd31cd9b7c8c53/...
    # ...Lib/logging/__init__.py#L704
    service: str
    asctime: Optional[str] = None
    levelname: str
    name: str
    filename: str
    funcName: str
    lineno: int
    message: str

    class Config:
        orm_mode = True

    @pydantic.validator("service")
    def check_service(value) -> str:
        """Validate the service field against standardized log service values."""
        if value not in OnclusiveService.list():
            raise ValueError(
                f"The specified service reference {value} is not in the valid range: "
                f"{OnclusiveService.list()}"
            )

        return value


class OnclusiveJSONFormatter(logging.Formatter):
    """Standard JSON log record formatter for all onclusive python (ML) applications.

    Can be subclassed by overloading the
    - `log_record_data_model` attributes and the
    - `formatMessage` method
    with custom data model and logic, respectively.
    """

    log_record_data_model = OnclusiveJSONLogRecord

    def __init__(
        self,
        service: str,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        validate: bool = True,
    ) -> None:
        super().__init__(fmt, datefmt, style, validate)

        self.service = service

    def _add_service_attribute(self, record: logging.LogRecord) -> logging.LogRecord:
        """Creates a LogRecord copy with an additional `service` attribute.

        Args:
            record (logging.LogRecord): A logging.LogRecord instance

        Returns:
            logging.LogRecord: A logging.LogRecord instance with an updated `service` attribute.
        """
        record_copy = copy(record)
        record_copy.__dict__.update({"service": self.service})

        return record_copy

    def _jsonify_record(self, record: logging.LogRecord) -> str:
        """Takes a record instance and converts it into a JSON string.

        Args:
            record (logging.LogRecord): The log record that is converted to JSON string.

        Returns:
            json_record (str): The JSON string version of the log record.
        """
        json_record = self.log_record_data_model.from_orm(record).json()

        return json_record

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Extends the `formatMessage` method with JSON conversion using OnclusiveJSONLogRecord.

        Args:
            record (logging.LogRecord): The log record that is converted to JSON.

        Returns:
            json_record (str): The JSON string version of the log record.
        """
        record.message = super().formatMessage(record)

        record_copy = self._add_service_attribute(record)

        json_record = self._jsonify_record(record_copy)

        return json_record
