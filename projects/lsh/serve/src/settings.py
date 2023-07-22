"""Settings."""

# Standard Library
from functools import lru_cache
from typing import Optional

# 3rd party libraries
from pydantic import BaseSettings


class Settings(BaseSettings):
    """API configuration."""

    # Generic settings
    # API name
    API_NAME: str = "LSH API"
    # API description
    API_DESCRIPTION: str = ""
    # API environment
    ENVIRONMENT: str = "dev"
    # Betterstack heartbeat key
    BETTERSTACK_KEY: str = ""
    # Debug level
    DEBUG: bool = True
    # API runtime
    KUBERNETES_IN_POD: bool = False
    # Logging level
    LOGGING_LEVEL: str = "info"
    # documentation endpoint
    DOCS_URL: Optional[str] = None
    # lsh endpoint
    LSH_ENDPOINT: str = "https://eks-data-prod.onclusive.com/lsh"

    API_KEY_NAME: str = "x-api-key"


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated Settings class."""
    return Settings()


settings = get_settings()
