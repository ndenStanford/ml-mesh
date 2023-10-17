"""Logger."""

# Standard Library
import logging
from typing import Optional

# Internal libraries
from onclusiveml.core.logging.constants import DEBUG, OnclusiveLogMessageFormats
from onclusiveml.core.logging.handlers import get_default_handler
from onclusiveml.core.logging.params import OnclusiveLogSettings


def get_default_logger(
    name: str,
    level: int = DEBUG,
    fmt_level: str = OnclusiveLogMessageFormats.SIMPLE.name,
    handler: Optional[logging.Handler] = None,
    json: bool = True,
) -> logging.Logger:
    """Utility for an opionated logger that encourages Onclusive ML app logging conventions.

    Those conventions are
    - a formatter using
        - one of the templates defined in OnclusiveLogMessageFormats
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
        fmt_level (Optional[str], optional): The log message format type to be used. Only used if
            the `handler` arg is not specified. The type gets mapped onto a valid format using the
            OnclusiveLogMessageFormats class. Defaults to `OnclusiveLogMessageFormats.SIMPLE.name`.
        handler (Optional[logging.Handler], optional): The logger handler to be used. If not
            specified, falls back on the returns of `get_default_streamhandler` with provided
            `level`, `fmt` and `json` arguments. Defaults to None.
        json (bool): Whether to use the OnclusiveJSONFormatter or standard Formatter. Defalts to
            True.

    Returns:
        logger (logging.Logger): A configured logger instance.
    """
    # validate inputs
    OnclusiveLogSettings(name=name, level=level, fmt_level=fmt_level, json=json)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # resolve format
    fmt = OnclusiveLogMessageFormats[fmt_level].value

    # clear any and all handlers to avoid duplication when calling this method repeatedly
    existing_handlers = logger.handlers

    for existing_handler in existing_handlers:
        logger.removeHandler(existing_handler)

    # if no handler is specified, create a configured one using handler util
    if handler is None:
        handler = get_default_handler(level=level, fmt=fmt, json=json)

    logger.addHandler(handler)

    return logger


def get_default_logger_from_env(
    name: str,
    handler: Optional[logging.Handler] = None,
) -> logging.Logger:
    """Utility for outputs of `get_default_logger` using environment variables.

    For details on the associated environment variables, see the OnclusiveLogSettings class.

    Args:
        name (str): The name of the logger.
        handler (Optional[logging.Handler], optional): The logger handler to be used. If not
            specified, falls back on the returns of `get_default_streamhandler` with `level`, `fmt`
            and `json` arguments parsed from the associated environment variables. Defaults to None.

    Returns:
        logger (logging.Logger): A configured logger instance.
    """
    logging_settings = OnclusiveLogSettings()

    logger = get_default_logger(name=name, handler=handler, **logging_settings)

    return logger
