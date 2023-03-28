"""Settings."""

# Standard Library
from typing import Optional

# 3rd party libraries
from pydantic import BaseSettings


class Settings(BaseSettings):
    """API configuration."""

    # Generic settings

    # api name
    API_NAME: str = "Keybert Prediction"

    # api description
    API_DESCRIPTION: str = ""

    # api environment
    ENVIRONMENT: str = "stage"

    # api debug level
    DEBUG: bool = True

    # api runtime
    KUBERNETES_IN_POD: bool = False

    # log level
    LOGGING_LEVEL: str = "info"

    # documentation endpoint
    DOCS_URL: Optional[str] = None

    # Keybert settings

    # Keybert base
    MODEL_NAME: str = "paraphrase-multilingual-MiniLM-L12-v2"


settings = Settings()
