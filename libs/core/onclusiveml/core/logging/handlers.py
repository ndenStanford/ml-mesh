"""Logging handlers."""

# Standard Library
import logging
import sys

# Internal libraries
from onclusiveml.core.logging.constants import (
    DEBUG,
    OnclusiveLogMessageFormat,
    OnclusiveService,
)
from onclusiveml.core.logging.formatters import (
    OnclusiveFormatter,
    OnclusiveJSONFormatter,
)


def get_default_handler(
    service: str = OnclusiveService.DEFAULT,
    level: int = DEBUG,
    fmt_level: OnclusiveLogMessageFormat = OnclusiveLogMessageFormat.DEFAULT,
    json_format: bool = True,
) -> logging.Handler:
    """Returns a logging Handler that defaults to onclusive ML JSON formatting conventions.

    Args:
        service (str): The onclusive ML service name for the JSON logs. Only relevant if
            `json_format`=True. Defaults to `OnclusiveService.DEFAULT.value`.
        level (int): Log level for handler. Defaults to 10.
        fmt_level (OnclusiveLogMessageFormat.SIMPLE): The message formatting level. The level
            gets mapped onto a valid format using the OnclusiveLogMessageFormat class. Defaults
            to `OnclusiveLogMessageFormat.SIMPLE`, which is mapped onto
            `OnclusiveLogMessageFormat.SIMPLE`
        json_format (bool, optional): Whether to use the OnclusiveJSONFormatter. Defaults to True.

    Returns:
        logging.Handler: A configured handler instance.
    """
    if json_format:
        formatter = OnclusiveJSONFormatter(service=service, fmt=fmt_level.value)
    else:
        formatter = OnclusiveFormatter(service=service, fmt=fmt_level.value)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    return handler
