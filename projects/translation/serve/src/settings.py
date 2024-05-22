"""Settings."""

# Standard Library
from functools import lru_cache

# 3rd party libraries
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings


class Boto3ClientSettings(OnclusiveBaseSettings):
    """App base settings."""

    region_name: str = "us-east-1"
    service_name: str = "translate"


class ModelSettings(OnclusiveBaseSettings):
    """Model Settings."""

    formality: str = "FORMAL"
    profanity: str = "MASK"
    model_name: str = "translation"
    api_version: int = 1


class GlobalSettings(
    Boto3ClientSettings,
    ModelSettings,
):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
