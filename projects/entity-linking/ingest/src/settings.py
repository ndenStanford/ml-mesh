"""Settings."""

# Standard Library
from functools import lru_cache

# 3rd party libraries
from pydantic import BaseSettings


class EmbeddingsSettings(BaseSettings):
    """Embeddings settings."""

    INDEX_FILE: str
    EMBEDDINGS_FILE: str


class VectorDBSettings(BaseSettings):
    """Vector store settings."""

    INDEX_NAME: str = "Wiki_entities"
    REDIS_CONNECTION_STRING: str


class GlobalSettings(EmbeddingsSettings, VectorDBSettings):
    """Global settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated Settings class."""
    return GlobalSettings()
