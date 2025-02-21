"""Logging formatters."""

# Standard Library
import logging
from typing import Literal, Optional

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
from onclusiveml.core.logging.constants import OnclusiveService


class OnclusiveLogRecord(OnclusiveBaseModel):
    """Standard (base) log format schema for all onclusive python (ML) applications."""

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


class OnclusiveFormatter(logging.Formatter):
    """Default (base) formatter for onclusve ML apps for non-JSON logs."""

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

        self.service = OnclusiveService.from_value(service, raises_if_not_found=True)

    def _add_service_attribute(self, record: logging.LogRecord) -> logging.LogRecord:
        """Updates/creates a LogRecord's "service" and "asctime" attribute.

        Note: The latter is required as for the - logging.Formatter parent class - the addition of
        the `asctime` log record attribute is conditional on the log format containing the field,
        which is not desired in a production environment. Therefore we need to add this attribute
        manually to ensure its existence independent of the log format being used.

        Args:
            record (logging.LogRecord): A logging.LogRecord instance

        Returns:
            logging.LogRecord: A logging.LogRecord instance with an updated
                    - `service` and
                    - `asctime`
                attribute.
        """
        setattr(record, "service", self.service)
        setattr(record, "asctime", self.formatTime(record, self.datefmt))

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
    """Default (base) formatter for onclusve ML apps for non-JSON logs.

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
        json_record = self.log_record_data_model.model_validate(
            record
        ).model_dump_json()

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
