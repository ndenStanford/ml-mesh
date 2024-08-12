"""Settings."""

# Standard Library
from functools import lru_cache
from typing import Optional

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
    aws_profile: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None


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
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
