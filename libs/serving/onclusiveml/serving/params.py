# Standard Library
from typing import Dict, Optional, Union

# 3rd party libraries
from pydantic import BaseSettings


class FastAPISettings(BaseSettings):
    name: str = "fastapi-app-name"


class UvicornSettings(BaseSettings):
    http_port: int = 8000
    host: str = "0.0.0.0"
    log_config: Optional[Union[str, Dict]] = None
    workers: int = 1


class ServingParams(BaseSettings):

    add_liveness: bool = True
    add_readiness: bool = True
    # fastapi settings
    fastapi_settings: FastAPISettings = FastAPISettings()
    # uvicorn settings
    uvicorn_settings: UvicornSettings = UvicornSettings()

    class Config:
        env_prefix = "onclusiveml_serving_modelserver_"
        env_file_encoding = "utf-8"
