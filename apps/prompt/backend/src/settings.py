"""Settings."""

# Standard Library
import json
from functools import lru_cache
from typing import Dict, List, Optional

# 3rd party libraries
from pydantic import BaseSettings

# Source
from src.model.constants import ModelEnum
from src.prompt.constants import PromptEnum


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
    # OpenAI API key
    OPENAI_API_KEY: str
    OPENAI_MAX_TOKENS: int = 512
    OPENAI_TEMPERATURE: float = 0.7
    # Betterstack heartbeat key
    BETTERSTACK_KEY: str = ""

    OPENAI_PARAMETERS = json.dumps(
        {
            "max_tokens": OPENAI_MAX_TOKENS,
            "temperature": OPENAI_TEMPERATURE,
        }
    )
    # predefined models
    LIST_OF_MODELS: Dict[str, List[str]] = {
        "1": [ModelEnum.GPT3_5.value, OPENAI_PARAMETERS, 4098],
        "2": [ModelEnum.GPT4.value, OPENAI_PARAMETERS, 8192],
    }
    LIST_OF_PROMPTS: Dict[str, List[str]] = {
        "1": [PromptEnum.EN.value[0], PromptEnum.EN.value[1]]
    }

    AWS_REGION: str = "us-east-1"

    REDIS_CONNECTION_STRING: str = ""
    REDIS_TTL_SECONDS: int = 604800

    DB_HOST: Optional[str] = None
    CORS_ORIGIN: List[str] = ["*"]


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated Settings class."""
    return Settings()
