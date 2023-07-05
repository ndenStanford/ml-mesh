# Standard Library
from typing import Dict, Optional, Union

# 3rd party libraries
from pydantic import BaseSettings


class ServingBaseParams(BaseSettings):
    """Base class implementing the environment variable prefix"""

    class Config:
        env_prefix = "onclusiveml_serving_"
        env_file_encoding = "utf-8"


class FastAPISettings(ServingBaseParams):
    name: str = "fastapi-app-name"


class LogConfigSettings(ServingBaseParams):
    """Log config default settings. Taken from the uvicorn log configuration handling approach
    shown here: https://github.com/encode/uvicorn/blob/ffa5b1ac96b10976ed0e092a0bc1dd5526101356/...
        ...uvicorn/config.py#L74"""

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: Dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
        },
    }

    handlers: Dict = {
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
    }

    loggers: Dict = {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    }


class UvicornSettings(ServingBaseParams):
    """A settings wrapper around the uvicorn library's `Config` class's constructor arguments. Used
    to configure the `ModelServer`'s underlying uvicorn process. See https://github.com/encode/...
    uvicorn/blob/ffa5b1ac96b10976ed0e092a0bc1dd5526101356/uvicorn/config.py#L187 for details.
    """

    http_port: int = 8000
    host: str = "0.0.0.0"
    log_config: Optional[Union[str, Dict]] = LogConfigSettings().dict()
    workers: int = 1


class ServingParams(ServingBaseParams):
    """A functional base class for specifying a configuration for the `ModelServer` constructor
    method's `configuration` argument"""

    add_liveness: bool = True
    add_readiness: bool = True
    add_model_predict: bool = True
    add_model_bio: bool = True
    api_version: str = "v1"

    # fastapi settings
    fastapi_settings: FastAPISettings = FastAPISettings()

    # uvicorn settings
    uvicorn_settings: UvicornSettings = UvicornSettings()
