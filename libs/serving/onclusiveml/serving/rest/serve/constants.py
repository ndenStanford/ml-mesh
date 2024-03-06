"""Constants."""

# Standard Library
from typing import Any, Dict

# Internal libraries
from onclusiveml.core.base import OnclusiveEnum
from onclusiveml.core.logging.constants import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    OnclusiveLogMessageFormat,
    OnclusiveService,
)


class OnclusiveServingLogMessageFormat(OnclusiveEnum):
    """Standardized log message formats for model servers."""

    # keep `levelprefix` & `status_code` to retain colouring feature using uvicorn formatters
    DEFAULT = "%(levelprefix)s %(asctime)s - %(message)s"
    ACCESS = '%(levelprefix)s %(asctime)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    # json string is uncoloured, so use default `levelname` and split status information into
    # `status_code` integer type and `status_phrase` string type
    DEFAULT_JSON = OnclusiveLogMessageFormat.DEFAULT.value
    ACCESS_JSON = '%(client_addr)s - "%(request_line)s" %(status_code)d %(status_phrase)s'  # noqa: E501


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
        "fmt": OnclusiveServingLogMessageFormat.DEFAULT.value,  # type: ignore[attr-defined]
        "use_colors": None,
    },
    "access": {
        "()": "uvicorn.logging.AccessFormatter",
        "fmt": OnclusiveServingLogMessageFormat.ACCESS.value,  # type: ignore[attr-defined]
    },
}

JSON_MODEL_SERVER_LOGGING_CONFIG = BASE_MODEL_SERVER_LOGGING_CONFIG.copy()
JSON_MODEL_SERVER_LOGGING_CONFIG["formatters"] = {
    "default": {
        "()": "onclusiveml.core.logging.OnclusiveJSONFormatter",
        "fmt": OnclusiveServingLogMessageFormat.DEFAULT_JSON.value,
        "service": OnclusiveService.DEFAULT.value,
    },
    "access": {
        "()": "onclusiveml.serving.rest.observability.OnclusiveServingJSONAccessFormatter",
        "fmt": OnclusiveServingLogMessageFormat.ACCESS_JSON.value,  # type: ignore[attr-defined]
        "service": OnclusiveService.DEFAULT.value,
    },
}
