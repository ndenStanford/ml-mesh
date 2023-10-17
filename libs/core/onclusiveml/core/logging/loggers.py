"""Logger."""

# Standard Library
import logging
from logging import config as log_config
from typing import Dict, Optional

# Internal libraries
from onclusiveml.core.logging.constants import OnclusiveLogMessageFormats
from onclusiveml.core.logging.formatters import OnclusiveJSONFormatter
from onclusiveml.core.logging.params import OnclusiveLogConfig


def get_logging_config(
    name: str,
    level: Optional[int] = None,
    handler: Optional[logging.Handler] = None,
    fmt: Optional[str] = None,
) -> Dict:
    """Returns an opinionated logging config that encourages Onclusive ML app logging conventions.

    Those conventions are
    - a formatter using
        - one of the templates defined in OnclusiveLogMessageFormats
        - JSON formatting of logs records as defined in the classes OnclusiveJSONLogRecord and
            OnclusiveJSONFormatter
    - a streamhandler writing to sys.stdout. This can be overridden by passing a Streamhandler
        instance to the `handler` arg (see below)

    Integrates with the environment variable entrypoint class OnclusiveLogConfig to provide default
    values derived from associated environment variables for easier configuration during deployment.

    Args:
        name (str): The name of the logger.
        level (Optional[int], optional): The log level to be used for the logger. Only used for the
            handler if `handler` arg is not specified. If `level` is not specified, uses the
            OnclusiveLogConfig to resolve a fallback value. In that case, if the associated
            environment variable `onclusiveml_core_logging_config_level` is undefined, resolves to
            DEBUG. Defaults to None.
        fmt (Optional[str], optional): The log message format to be used. Only used if the `handler`
            arg is not specified. If `fmt` is not specified, uses the OnclusiveLogConfig to resolve
            a fallback value. In that case, if the associated environment variable
            `onclusiveml_core_logging_config_format_type` is undefined, resolves to
            "%(asctime)s - %(levelname)s - %(message)s". Defaults to None.
        handler (Optional[logging.Handler], optional): The logger handler to be used. If not
            specified, falls back on a StreamHandler with
                - sys.stdout stream using the
                - OnclusiveJSONFormatter for JSON formatting, and
                - the resolved level value (see above) as level
            Defaults to None.

    Returns:
        Dict: A functioning logging config dictionary.
    """
    if level is None:
        level = OnclusiveLogConfig().log_level

    if fmt is None:
        message_format_type = OnclusiveLogConfig().format_type
        fmt = OnclusiveLogMessageFormats[message_format_type].value

    if handler is None:
        handler_config = {
            "formatter": "onclusive_json_formatter",
            "class": "logging.StreamHandler",
            "level": level,
            "stream": "ext://sys.stdout",
        }
    else:
        handler_config = {
            "()": lambda: handler,
        }

    logging_config = {
        "version": 1,
        "formatters": {
            "onclusive_json_formatter": {
                "()": lambda: OnclusiveJSONFormatter(fmt=fmt),
            },
        },
        "handlers": {
            "console": handler_config,
        },
        "loggers": {
            f"{name}": {
                "handlers": ["console"],
                "level": level,
                "propagate": True,
            },
        },
    }

    return logging_config


def get_default_logger(
    name: str,
    level: Optional[int] = None,
    fmt: Optional[str] = None,
    handler: Optional[logging.Handler] = None,
) -> logging.Logger:
    """Utility for an opionated logger that encourages Onclusive ML app logging conventions.

    Those conventions are
    - a formatter using
        - one of the templates defined in OnclusiveLogMessageFormats
        - JSON formatting of logs records as defined in the classes OnclusiveJSONLogRecord and
            OnclusiveJSONFormatter
    - a streamhandler writing to sys.stdout. This can be overridden by passing a Streamhandler
        instance to the `handler` arg (see below)

    Integrates with the environment variable entrypoint class OnclusiveLogConfig to provide default
    values derived from associated environment variables for easier configuration during deployment.

    Args:
        name (str): The name of the logger.
        level (Optional[int], optional): The log level to be used for the logger. Only used for the
            handler if `handler` arg is not specified. If `level` is not specified, uses the
            OnclusiveLogConfig to resolve a fallback value. In that case, if the associated
            environment variable `onclusiveml_core_logging_config_level` is undefined, resolves to
            DEBUG. Defaults to None.
        fmt (Optional[str], optional): The log message format to be used. Only used if the `handler`
            arg is not specified. If `fmt` is not specified, uses the OnclusiveLogConfig to resolve
            a fallback value. In that case, if the associated environment variable
            `onclusiveml_core_logging_config_format_type` is undefined, resolves to
            "%(asctime)s - %(levelname)s - %(message)s". Defaults to None.
        handler (Optional[logging.Handler], optional): The logger handler to be used. If not
            specified, falls back on a StreamHandler with
                - sys.stdout stream using the
                - OnclusiveJSONFormatter for JSON formatting, and
                - the resolved level value (see above) as level
            Defaults to None.

    Returns:
        logger (logging.Logger): A configured logger instance.
    """
    # assemble logging config
    onclusive_logging_config = get_logging_config(
        name,
        handler=handler,
        fmt=fmt,
        level=level,
    )
    # apply logging config
    log_config.dictConfig(onclusive_logging_config)

    logger = logging.getLogger(name)

    return logger
