"""Logging handlers."""

# Standard Library
import logging
import sys

# Internal libraries
from onclusiveml.core.logging.constants import DEBUG, OnclusiveLogMessageFormat
from onclusiveml.core.logging.formatters import OnclusiveJSONFormatter


def get_default_handler(
    level: int = DEBUG,
    fmt_level: str = OnclusiveLogMessageFormat.SIMPLE.name,
    json_format: bool = True,
) -> logging.Handler:
    """Returns a logging Handler that defaults to onclusive ML JSON formatting conventions.

    Args:
        level (int): Log level for handler. Defaults to 10.
        fmt_level (OnclusiveLogMessageFormat.SIMPLE.name): The message formatting level. The level
            gets mapped onto a valid format using the OnclusiveLogMessageFormat class. Defaults
            to `OnclusiveLogMessageFormat.SIMPLE.name`, which is mapped onto
            `OnclusiveLogMessageFormat.SIMPLE.value`
        json_format (bool, optional): Whether to use the OnclusiveJSONFormatter. Defaults to True.

    Returns:
        logging.Handler: A configured handler instance.
    """
    # resolve format
    fmt = OnclusiveLogMessageFormat[fmt_level].value

    if json_format:
        formatter = OnclusiveJSONFormatter(fmt=fmt)
    else:
        formatter = logging.Formatter(fmt=fmt)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    return handler
