"""Logging formatters."""

# Standard Library
import logging
from typing import Literal, Optional

# 3rd party libraries
import pydantic

# Internal libraries
from onclusiveml.core.logging.constants import OnclusiveService


class OnclusiveLogRecord(pydantic.BaseModel):
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


class OnclusiveFormatter(logging.Formatter):
    """Default formatter for onclusve ML apps for non-JSON logs."""

    log_record_data_model = OnclusiveLogRecord

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
        """Updates/creates a LogRecord's "service" attribute.

        Args:
            record (logging.LogRecord): A logging.LogRecord instance

        Returns:
            logging.LogRecord: A logging.LogRecord instance with an updated `service` attribute.
        """
        setattr(record, "service", self.service)

        return record

    def _format_record(self, record: logging.LogRecord) -> logging.LogRecord:
        """Adds `service` attribute to record, then formats its message attribute.

        Args:
            record (logging.LogRecord): The log record that needs formatting.

        Returns:
            record (logging.LogRecord): The formatted log record.
        """
        record = self._add_service_attribute(record)

        record.message = super().formatMessage(record)

        return record

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Adds `service` attribute to record, then formats and returns its message attribute.

        Args:
            record (logging.LogRecord): The log record that is converted to JSON.

        Returns:
            formatted_record.message (str): The formatted message of the log record.
        """
        formatted_record = self._format_record(record)

        return formatted_record.message


class OnclusiveJSONFormatter(OnclusiveFormatter):
    """Default formatter for onclusve ML apps for non-JSON logs.

    Can be subclassed by overloading the
    - `log_record_data_model` attributes and the
    - `formatMessage` method
    with custom data model and logic, respectively.
    """

    def _jsonify_record(self, record: logging.LogRecord) -> str:
        """Takes a log record instance and converts it into a JSON string.

        The log record must contain all fields of the OnclusiveLogRecord schema.

        Args:
            record (logging.LogRecord): The log record that is converted to JSON string.

        Returns:
            json_record (str): The JSON string version of the log record.
        """
        json_record = self.log_record_data_model.from_orm(record).json()

        return json_record

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Extends the OnclusiveFormatter.formatMessage with a JSON conversion step.

        Args:
            record (logging.LogRecord): The log record that is converted to JSON string.

        Returns:
            json_message: The formatted log record message in JSON format.
        """
        formatted_record = super()._format_record(record)

        json_message = self._jsonify_record(formatted_record)

        return json_message
