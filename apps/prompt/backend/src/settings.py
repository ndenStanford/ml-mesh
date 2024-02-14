"""Settings."""

# Standard Library
import json
from functools import lru_cache
from typing import Dict, List, Optional, Union

# 3rd party libraries
from pydantic import Field, SecretStr

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings

# Source
from src.model.constants import ModelEnumChat, ModelEnumCompletions
from src.prompt.constants import PromptEnum


class GithubSettings(OnclusiveBaseSettings):
    """Credentials for Github reposotory."""

    github_token: SecretStr = Field(default="github_token", exclude=True)
    github_url: str = "AirPR/ml-prompt-registry"

    class Config:
        env_prefix = "onclusiveml_prompt_repo_"


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
    OPENAI_MAX_TOKENS: int = 512
    OPENAI_TEMPERATURE: float = 0.7
    RESPONSE_FORMAT: Optional[Dict] = None
    # Betterstack heartbeat key
    BETTERSTACK_KEY: str = ""

    OPENAI_PARAMETERS = json.dumps(
        {
            "max_tokens": OPENAI_MAX_TOKENS,
            "temperature": OPENAI_TEMPERATURE,
            "response_format": RESPONSE_FORMAT,
        }
    )
    # predefined models
    LIST_OF_MODELS: Dict[str, List[Union[str, int]]] = {
        "1": [ModelEnumChat.GPT3_5.value, OPENAI_PARAMETERS, 4098],
        "2": [ModelEnumChat.GPT4.value, OPENAI_PARAMETERS, 8192],
        "3": [ModelEnumChat.GPT3_5_turbo.value, OPENAI_PARAMETERS, 16385],
        "4": [ModelEnumChat.GPT4_turbo.value, OPENAI_PARAMETERS, 128000],
        "5": [ModelEnumCompletions.GPT3_5_instruct.value, OPENAI_PARAMETERS, 4096],
    }

    LIST_OF_PROMPTS: List[List[Union[str, Dict]]] = PromptEnum.list()

    AWS_REGION: str = "us-east-1"

    REDIS_CONNECTION_STRING: str = ""
    REDIS_TTL_SECONDS: int = 604800

    DB_HOST: Optional[str] = None
    CORS_ORIGIN: List[str] = ["*"]

    github_credentials: GithubSettings


@lru_cache
def get_settings() -> Settings:
    """Returns instanciated Settings class."""
    github_credentials = GithubSettings()
    return Settings(github_credentials=github_credentials)
