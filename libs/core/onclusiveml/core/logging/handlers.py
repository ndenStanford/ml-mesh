"""Logging handlers."""

# Standard Library
import logging
import sys

# Internal libraries
from onclusiveml.core.logging.constants import DEBUG, OnclusiveLogMessageFormats
from onclusiveml.core.logging.formatters import OnclusiveJSONFormatter


def get_default_handler(
    level: int = DEBUG,
    fmt: str = OnclusiveLogMessageFormats.SIMPLE.value,
    json: bool = True,
) -> logging.Handler:
    """Returns a logging Handler that defaults to onclusive ML JSON formatting conventions.

    Args:
        level (int): Log level for handler. Defaults to 10.
        fmt (OnclusiveLogMessageFormats.SIMPLE.value): The message formatting template. Defaults to
            `OnclusiveLogMessageFormats.SIMPLE.value`.
        json (bool, optional): Whether to use the OnclusiveJSONFormatter. Defaults to True.

    Returns:
        logging.Handler: A configured handler instance.
    """
    if json:
        formatter = OnclusiveJSONFormatter(fmt=fmt)
    else:
        formatter = logging.Formatter(fmt=fmt)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    return handler
