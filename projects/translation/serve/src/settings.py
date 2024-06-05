"""Settings."""

# Standard Library
from functools import lru_cache

# 3rd party libraries
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.serving.rest.serve.params import ServingParams


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "translation"


class Boto3ClientSettings(OnclusiveBaseSettings):
    """App base settings."""

    region_name: str = "us-east-2"
    service_name: str = "translate"


class ModelSettings(OnclusiveBaseSettings):
    """Model Settings."""

    profanity: str = "MASK"
    model_name: str = "translation"


class GlobalSettings(
    ServerModelSettings,
    Boto3ClientSettings,
    ModelSettings,
):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
