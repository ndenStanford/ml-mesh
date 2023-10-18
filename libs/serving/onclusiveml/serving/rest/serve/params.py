"""Serving parameters."""

# Standard Library
from typing import Dict, Optional, Union

# 3rd party libraries
from pydantic import Field, SecretStr, root_validator

# Internal libraries
from onclusiveml.serving.params import ServingBaseParams


class FastAPISettings(ServingBaseParams):
    """Fastapi test settings."""

    name: str = "fastapi-app-name"

    class Config:
        env_prefix = f"{ServingBaseParams.Config.env_prefix}fastapi_"
        env_file_encoding = "utf-8"


class LogConfigSettings(ServingBaseParams):
    """Logging settings for the uvicorn server loggers."""

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

    http_port: int = 8000
    host: str = "0.0.0.0"
    log_config: Optional[Union[str, Dict]] = LogConfigSettings().dict()
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
