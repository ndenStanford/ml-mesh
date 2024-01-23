"""Serving parameters."""

# Standard Library
from typing import Dict, List, Optional, Union

# 3rd party libraries
from pydantic import Field, SecretStr, root_validator

# Internal libraries
from onclusiveml.core.logging import INFO, OnclusiveService
from onclusiveml.serving.params import ServingBaseParams
from onclusiveml.serving.rest.serve.constants import (
    DEFAULT_MODEL_SERVER_LOGGING_CONFIG,
    JSON_MODEL_SERVER_LOGGING_CONFIG,
    LOG_LEVEL_MAP,
)


def get_logging_config(
    service: str = OnclusiveService.DEFAULT.value,
    level: int = INFO,
    json_format: bool = True,
) -> Dict:
    """Returns a logging config for the uvicorn server underpinning running the ModelServer.

    Returns a manipulated version of uvicorn.config.LOGGING_CONFIG to ensure uvicorn server logs
    adhere to internal formatting conventions.

    If `json_format` is set to True, additionally updates the uvicorn.config.LOGGING_CONFIG
    dictionary to use internal JSON formatting utilities
        - OnclusiveServingJSONDefaultFormatter, and
        - OnclusiveServingJSONAccessFormatter
    to ensure that uvicorn server log format is a strucutred JSON string

    Args:
        service (str): The onclusive ML service name for the JSON logs. Only relevant if
            `json_format`=True. Defaults to `OnclusiveService.DEFAULT.value`.
        level (int): The log level that is universally applied to all uvicorn server level loggers:
            - uvicorn
            - uvicorn.error
            - uvicorn.access
        json_format (bool, optional): Whether te uvicorn server level loggers should use JSON
            formatting. Defaults to True.

    Returns:
        Dict: A functional logging config to configure uvicorn server logging behaviour that can be
            specified as the `log_config` argument to the `uvicorn.run` method.
    """
    # resolve json input -> config
    if json_format:
        logging_config = JSON_MODEL_SERVER_LOGGING_CONFIG
        # validate service name
        OnclusiveService.validate(service)
        # set service name
        for formatter in logging_config["formatters"].values():
            formatter["service"] = service
    else:
        logging_config = DEFAULT_MODEL_SERVER_LOGGING_CONFIG
    # set log level
    for logger in logging_config["loggers"].values():
        logger["level"] = LOG_LEVEL_MAP[level]

    return logging_config


class FastAPISettings(ServingBaseParams):
    """Fastapi test settings."""

    name: str = "fastapi-app-name"

    class Config:
        env_prefix = f"{ServingBaseParams.Config.env_prefix}fastapi_"
        env_file_encoding = "utf-8"


class LogConfigSettings(ServingBaseParams):
    """Logging settings for the uvicorn server loggers."""

    service: str = OnclusiveService.DEFAULT.value
    level: int = 20  # INFO
    json_format: bool = True

    class Config:
        env_prefix = f"{ServingBaseParams.Config.env_prefix}logconfig_"
        env_file_encoding = "utf-8"


class UvicornSettings(ServingBaseParams):
    """A settings wrapper around the uvicorn library's `Config` class's constructor arguments.

    Used to configure the `ModelServer`'s underlying uvicorn process.

    References:
    https://github.com/encode/uvicorn/blob/ffa5b1ac96b10976ed0e092a0bc1dd5526101356/...
    uvicorn/config.py#L187
    """

    app: str = "src.serve.model_server:model_server"
    port: int = 8000
    host: str = "0.0.0.0"
    log_config: Optional[Union[str, Dict]] = Field(
        default_factory=lambda: get_logging_config(**LogConfigSettings().dict())
    )
    reload: bool = False
    reload_dirs: Optional[Union[List[str], str]] = None
    reload_delay: float = 0.25
    reload_includes: Optional[Union[List[str], str]] = None
    reload_excludes: Optional[Union[List[str], str]] = None
    workers: int = 1

    class Config:
        env_prefix = f"{ServingBaseParams.Config.env_prefix}uvicorn_"
        env_file_encoding = "utf-8"


class BetterStackSettings(ServingBaseParams):
    """Settings class for betterstack integration.

    Attributes:
        enable (bool): A switch for enabling/disabling betetrstack heartbeat check.
        api_token (str): Token to authenticate with betterstack and identify the betterstack
            project.
        base_url (str): The base url of the betterstack service we want to submit a liveness pulse
            to
        full_url (str): The full url of the betterstack service we want to submit a liveness pulse
            to, including the api_token. See `assemble_betterstack_url` for details.
    """

    enable: bool = False
    api_token: SecretStr = Field("dummy_api_token", exclude=True)
    base_url: str = "https://uptime.betterstack.com/api/v1/heartbeat/"
    full_url: str = ""

    class Config:
        env_prefix = f"{ServingBaseParams.Config.env_prefix}betterstack_"
        env_file_encoding = "utf-8"

    @root_validator
    def assemble_betterstack_url(cls, values: Dict) -> Dict:
        """Assembles the full_url field using the two fields.

        Uses attributes
        - base_url
        - api_token

        as per full_url = {base_url}{api_token}

        Args:
            values (Dict): Dictionary containing all field values at time of initialization

        Returns:
            values (Dict): A dictionary containing all field values, with the full_url dynamically
                populated
        """
        base_url = values.get("base_url")
        api_token = values.get("api_token").get_secret_value()  # type: ignore[union-attr]

        values["full_url"] = f"{base_url}{api_token}"

        return values


class ServingParams(ServingBaseParams):
    """Base class for the `ModelServer` configuration for the constructor method's.

    Note:
        This configuration is passed via the  `configuration` argument of the method.
    """

    add_liveness: bool = True
    add_readiness: bool = True
    add_model_predict: bool = True
    add_model_bio: bool = True
    api_version: str = "v1"
    # fastapi settings
    fastapi_settings: FastAPISettings = FastAPISettings()
    # uvicorn settings
    uvicorn_settings: UvicornSettings = UvicornSettings()
    # betterstack settings
    betterstack_settings = BetterStackSettings()
    # test inference for readiness/liveness probe
    sample_inference_during_readiness: bool = False
    sample_inference_during_liveness: bool = False
