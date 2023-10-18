"""Constants."""
# Standard Library
from typing import Any, Dict

# Internal libraries
from onclusiveml.core.base.utils import OnclusiveEnum
from onclusiveml.core.logging.constants import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
)


class OnclusiveModelServerLogMessageFormat(OnclusiveEnum):
    """Standardized log message formats for model servers."""

    ACCESS = '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    DEFAULT = "%(levelprefix)s %(message)s"


LOG_LEVEL_MAP: Dict[int, str] = {
    DEBUG: "DEBUG",
    INFO: "INFO",
    WARNING: "WARNING",
    ERROR: "ERROR",
    CRITICAL: "CRITICAL",
}

BASE_MODEL_SERVER_LOGGING_CONFIG: Dict[Any, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}

DEFAULT_MODEL_SERVER_LOGGING_CONFIG = BASE_MODEL_SERVER_LOGGING_CONFIG.copy()
DEFAULT_MODEL_SERVER_LOGGING_CONFIG["formatters"] = {
    "default": {
        "()": "uvicorn.logging.DefaultFormatter",
        "fmt": OnclusiveModelServerLogMessageFormat.DEFAULT,
        "use_colors": None,
    },
    "access": {
        "()": "uvicorn.logging.AccessFormatter",
        "fmt": OnclusiveModelServerLogMessageFormat.ACCESS,  # noqa: E501
    },
}

JSON_MODEL_SERVER_LOGGING_CONFIG = BASE_MODEL_SERVER_LOGGING_CONFIG.copy()
JSON_MODEL_SERVER_LOGGING_CONFIG["handlers"] = {
    "default": {
        "()": "onclusiveml.serving.rest.observability.OnclusiveServingJSONDefaultFormatter",
        "fmt": OnclusiveModelServerLogMessageFormat.DEFAULT,
        "use_colors": None,
    },
    "access": {
        "()": "onclusiveml.serving.rest.observability.OnclusiveServingJSONAccessFormatter",
        "fmt": OnclusiveModelServerLogMessageFormat.ACCESS,
    },
}
