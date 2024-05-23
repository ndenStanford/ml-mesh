"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import List, Union

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import BaseSettings, Field

# Internal libraries
from onclusiveml.tracking import TrackedModelSpecs


class EmbeddingsSettings(BaseSettings):
    """Embeddings settings."""

    INDEX_FILE: str = ""
    EMBEDDINGS_FILE: str = ""
    EMBEDDINGS_SHAPE: List = [16470856, 300]


class VectorDBSettings(BaseSettings):
    """Vector store settings."""

    INDEX_NAME: str = "Wiki_entities"
    REDIS_CONNECTION_STRING: str = ""


class TrackedTrainedModelSpecs(TrackedModelSpecs):
    """Tracked compiled model settings."""

    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = Field("EL-TRAINED-22", env="neptune_model_version_id")
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY, env="neptune_client_mode")
    model_name: str = "entity-linking"
    model_directory: Union[str, Path] = "./models"


class GlobalSettings(EmbeddingsSettings, VectorDBSettings, TrackedTrainedModelSpecs):
    """Global settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated Settings class."""
    return GlobalSettings()
