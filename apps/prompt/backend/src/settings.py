"""Settings."""

# Standard Library
import json
from functools import lru_cache
from typing import Dict, List, Optional, Union

# 3rd party libraries
from pydantic import Field, SecretStr

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings


class Settings(OnclusiveBaseSettings):
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
    LLM_CALL_RETRY_COUNT: int = 2
    # Betterstack heartbeat key
    BETTERSTACK_KEY: str = ""

    REDIS_CONNECTION_STRING: str = ""
    REDIS_TTL_SECONDS: int = 604800

    DYNAMODB_HOST: Optional[str] = None
    AWS_DEFAULT_REGION: str = "us-east-1"

    CORS_ORIGIN: List[str] = ["*"]

    GITHUB_TOKEN: SecretStr = Field(default="github_token")
    GITHUB_URL: str = "AirPR/ml-prompt-registry"


@lru_cache
def get_settings() -> Settings:
    """Returns instanciated Settings class."""
    return Settings()
