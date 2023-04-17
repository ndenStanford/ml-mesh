"""Settings."""

# Standard Library
from functools import lru_cache
from typing import Dict, Optional

# 3rd party libraries
from pydantic import BaseSettings


class Settings(BaseSettings):
    """API configuration."""

    # Generic settings
    # api name
    API_NAME: str = "Prompt Manager"

    # api description
    API_DESCRIPTION: str = ""

    # api environment
    ENVIRONMENT: str = "dev"

    # api debug level
    DEBUG: bool = True

    # api runtime
    KUBERNETES_IN_POD: bool = False

    # log level
    LOGGING_LEVEL: str = "debug"

    # documentation endpoint
    DOCS_URL: Optional[str] = None

    # initialize database
    INITIALIZE: bool = True

    # API key for secure endpoints access
    API_KEY: str
    API_KEY_NAME: str = "x-api-key"

    # OpenAI API key
    OPENAI_API_KEY: str
    OPENAI_MAX_TOKENS: int = 512
    OPENAI_TEMPERATURE: float = 0.7

    # predefined models
    LIST_OF_MODELS: Dict[str, str] = {
        "1": "gpt-3.5.turbo",
        "2": "text-davinci-003",
        "3": "text-curie-001",
        "4": "gpt-4",
    }

    AWS_REGION: str = "us-east-1"

    DB_HOST: Optional[str] = None


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated Settings class."""
    return Settings()
