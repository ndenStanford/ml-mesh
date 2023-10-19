"""Logger."""

# Standard Library
import logging
from typing import Optional

# Internal libraries
from onclusiveml.core.logging.constants import DEBUG, OnclusiveLogMessageFormat
from onclusiveml.core.logging.handlers import get_default_handler
from onclusiveml.core.logging.params import OnclusiveLogSettings


def get_default_logger(
    name: str,
    level: int = DEBUG,
    fmt_level: str = OnclusiveLogMessageFormat.SIMPLE.name,
    json_format: bool = True,
    handler: Optional[logging.Handler] = None,
) -> logging.Logger:
    """Utility for an opionated logger that encourages Onclusive ML app logging conventions.

    Those conventions are
    - a formatter using
        - one of the templates defined in OnclusiveLogMessageFormat
        - Optional: JSON formatting of logs records as defined in the classes OnclusiveJSONLogRecord
            and OnclusiveJSONFormatter
    - a streamhandler writing to sys.stdout.

    These can be overridden by passing a Streamhandler (or another handler type) instance to the
    `handler` arg (see below)

    Is idempotent w.r.t global logging configurations, i.e. calling this method more than once does
    not alter the global logging behaviour any more than just calling it once.

    Args:
        name (str): The name of the logger.
        level (Optional[int], optional): The log level to be used for the logger. Defaults to
            `DEBUG`.
        fmt_level (Optional[str], optional): The log message format level to be used. Only used if
            the `handler` arg is not specified.
        json_format (bool): Whether to use the OnclusiveJSONFormatter or standard Formatter. Defalts
            to True.
        handler (Optional[logging.Handler], optional): The logger handler to be used. If not
            specified, falls back on the returns of `get_default_streamhandler` with provided
            `level`, `fmt` and `json_format` arguments. Defaults to None.

    Returns:
        logger (logging.Logger): A configured logger instance.
    """
    # validate inputs
    log_settings = OnclusiveLogSettings(
        level=level, fmt_level=fmt_level, json_format=json_format
    )

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # clear any and all handlers to avoid duplication when calling this method repeatedly
    existing_handlers = logger.handlers

    for existing_handler in existing_handlers:
        logger.removeHandler(existing_handler)

    # if no handler is specified, create a configured one using handler util
    if handler is None:
        handler = get_default_handler(**log_settings.dict())

    logger.addHandler(handler)

    return logger


def get_default_logger_from_env(
    name: str,
) -> logging.Logger:
    """Environment variable based wrapper around `get_default_logger` function.

    For details on the associated environment variables, see the OnclusiveLogSettings class.

    Args:
        name (str): The name of the logger.

    Returns:
        logger (logging.Logger): A configured logger instance.
    """
    log_settings = OnclusiveLogSettings()

    logger = get_default_logger(name=name, handler=None, **log_settings.dict())

    return logger
