"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import Union

# 3rd party libraries
from pydantic import BaseSettings, SecretStr

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.serving.rest.serve.params import ServingParams


class ServedModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "entity-linking"
    model_directory: Union[str, Path] = "."


class ApplicationSettings(OnclusiveBaseSettings):
    """App base settings."""

    api_key_name: str = "x-api-key"
    entity_fishing_endpoint: str
    internal_ml_api_key: SecretStr
    entity_recognition_endpoint: str


class GlobalSettings(ServedModelSettings, ApplicationSettings):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
