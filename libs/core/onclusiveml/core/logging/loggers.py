"""Logger."""

# Standard Library
import logging
from typing import Optional

# Internal libraries
from onclusiveml.core.logging.constants import (
    LoggingLevel,
    OnclusiveLogMessageFormat,
    OnclusiveService,
)
from onclusiveml.core.logging.handlers import get_default_handler
from onclusiveml.core.logging.settings import OnclusiveLogSettings


def get_default_logger(
    name: str,
    service: str = OnclusiveService.DEFAULT,
    level: int = LoggingLevel.DEBUG.value,
    fmt_level: OnclusiveLogMessageFormat = OnclusiveLogMessageFormat.DEFAULT,
    json_format: bool = False,
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
        service (str): The onclusive ML service name for the JSON logs. Only relevant if
            `json_format`=True. Defaults to `OnclusiveService.DEFAULT`.
        level (Optional[int], optional): The log level to be used for the logger. Defaults to
            `DEBUG`.
        fmt_level (OnclusiveLogMessageFormat): The log message format level to be used. Only used if
            the `handler` arg is not specified.
        json_format (bool): Whether to use the OnclusiveJSONFormatter or standard Formatter. Defalts
            to True.
        handler (Optional[logging.Handler], optional): The logger handler to be used. If not
            specified, falls back on the returns of `get_default_streamhandler` with provided
            `level`, `fmt` and `json_format` arguments. Defaults to None.

    Returns:
        logger (logging.Logger): A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # clear any and all handlers to avoid duplication when calling this method repeatedly
    existing_handlers = logger.handlers

    for existing_handler in existing_handlers:
        logger.removeHandler(existing_handler)

    # if no handler is specified, create a configured one using handler util
    if handler is None:
        handler = get_default_handler(
            service=service, level=level, fmt_level=fmt_level, json_format=json_format
        )

    logger.addHandler(handler)

    return logger


def _set_root_verbosity(settings: OnclusiveLogSettings) -> None:
    """Set the root verbosity.

    Args:
        settings (OnclusiveLogSettings): logging settings
    """
    level = settings.level
    if level != LoggingLevel.NOTSET:
        logging.basicConfig(level=level)
        get_default_logger(__name__).debug(
            f"Logging set to level: " f"{logging.getLevelName(level)}"
        )
    else:
        logging.disable(sys.maxsize)
        logging.getLogger().disabled = True
        get_default_logger(__name__).debug("Logging NOTSET")


def init_logging(settings: OnclusiveLogSettings) -> None:
    """Initialize logging with default levels.

    Args:
        settings (OnclusiveLogSettings): logging settings
    """
    _set_root_verbosity(settings)

    for logger_name in settings.suppressed_logger_names:
        logging.getLogger(logger_name).setLevel(logging.INFO)

    for logger_name in settings.disabled_logger_names:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
        logging.getLogger(logger_name).disabled = True
