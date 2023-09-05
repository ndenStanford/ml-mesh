"""Settings."""

# Standard Library
from functools import lru_cache

# 3rd party libraries
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    """App base settings."""

    API_KEY_NAME: str = "x-api-key"
    ENTITY_FISHING_ENDPOINT: str
    INTERNAL_ML_ENDPOINT_API_KEY: SecretStr
    ENTITY_RECOGNITION_ENDPOINT: str


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated Settings class."""
    return Settings()
