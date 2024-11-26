"""Settings."""

# Standard Library
from functools import lru_cache
from typing import List, Optional

# 3rd party libraries
from pydantic import SecretStr

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
    CELERY_MAX_RETRY_COUNTS: int = 3
    CELERY_RETRY_DELAY: float = 30
    LLM_CALL_RETRY_COUNT: int = 2
    LLM_CALL_RETRY_DELAY: float = 3.0
    LLM_CALL_RETRY_BACKOFF: float = 2.0
    LLM_CALL_RETRY_MAX_DELAY: float = 10.0
    # Betterstack heartbeat key
    BETTERSTACK_KEY: str = ""

    REDIS_CONNECTION_STRING: str = ""
    REDIS_TTL_SECONDS: int = 86400

    DYNAMODB_HOST: Optional[str] = None
    AWS_DEFAULT_REGION: str = "us-east-1"
    AWS_PROFILE: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    DEFAULT_MODELS: dict = {"default": "gpt-4o-mini"}
    PROMPTS_TO_SYNC: List[str] = ["machine-learning/english-summarization"]
    CORS_ORIGIN: List[str] = ["*"]
    BEDROCK_READ_TIMEOUT: int = 300
    # Github configuration
    PROMPT_REGISTRY_APP_ID: str
    PROMPT_REGISTRY_APP_PRIVATE_KEY: SecretStr
    GITHUB_REPOSITORY: str = "AirPR/ml-prompt-registry"


@lru_cache
def get_settings() -> Settings:
    """Returns instanciated Settings class."""
    return Settings()
