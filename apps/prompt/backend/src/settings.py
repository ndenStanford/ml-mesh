"""Settings."""

# Standard Library
import json
from functools import lru_cache
from typing import Dict, List, Optional

# 3rd party libraries
from pydantic import BaseSettings

# Source
from src.model.constants import ModelEnum


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

    OPENAI_PARAMETERS = json.dumps(
        {
            "max_tokens": OPENAI_MAX_TOKENS,
            "temperature": OPENAI_TEMPERATURE,
        }
    )
    # predefined models
    LIST_OF_MODELS: Dict[str, List[str]] = {
        "1": [ModelEnum.GPT3_5.value, OPENAI_PARAMETERS],
        "2": [ModelEnum.DAVINCI.value, OPENAI_PARAMETERS],
        "3": [ModelEnum.CURIE.value, OPENAI_PARAMETERS],
        "4": [ModelEnum.GPT4.value, OPENAI_PARAMETERS],
    }

    AWS_REGION: str = "us-east-1"

    DB_HOST: Optional[str] = None

    CORS_ORIGIN: List[str] = ["http://localhost:3333", "localhost:3333"]


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated Settings class."""
    return Settings()
