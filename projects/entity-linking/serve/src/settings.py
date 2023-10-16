"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import List, Union

# 3rd party libraries
from pydantic import BaseSettings, SecretStr

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.serving.rest.serve.params import ServingParams


class KnowledgeGraphDataSettings(ServingParams):
    """Serve model parameters."""

    source_bucket: str = "onclusive-model-store-dev"
    source_path: str = "entity-fishing"
    target_path: str = "/opt/entity-fishing/data/db"
    knowledge_bases: List[str] = [
        "kb",
        "en",
    ]


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
    enable_metrics: bool = False


class GlobalSettings(
    ServedModelSettings, ApplicationSettings, KnowledgeGraphDataSettings
):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
