"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union

# 3rd party libraries
from pydantic import BaseSettings, SecretStr

# Internal libraries
from onclusiveml.serving.rest.serve.params import ServingParams


class Settings(BaseSettings):
    """API configuration."""

    # Generic settings
    # API name
    API_NAME: str = "Summarization Prediction"
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
    DOCS_URL: Optional[str] = "/summarization/docs"
    OPENAPI_URL: Optional[str] = "/summarization/openapi.json"
    # OpenAI api key
    OPENAI_API_KEY: str = ""
    # Prompt url
    PROMPT_API: str = "http://prompt-backend:4000"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "1234"
    SUMMARIZATION_DEFAULT_MODEL: str = "gpt-4o"

    PROMPT_DICT = {
        "en": {
            "en": {"alias": "ml-summarization-english"},
            "fr": {"alias": "ml-summarization-english-french"},
        },
        "fr": {
            "fr": {"alias": "ml-summarization-french"},
            "en": {"alias": "ml-summarization-french-english"},
        },
        "de": {"de": {"alias": "ml-summarization-german"}},
        "it": {"it": {"alias": "ml-summarization-italian"}},
        "es": {"es": {"alias": "ml-summarization-spanish"}},
        "ca": {"ca": {"alias": "ml-summarization-catalan"}},
        "pt": {"pt": {"alias": "ml-summarization-portuguese"}},
        "zh": {"zh": {"alias": "ml-summarization-chinese_simplified"}},
        "zh-t": {"zh-t": {"alias": "ml-summarization-chinese_traditional"}},
        "ja": {"ja": {"alias": "ml-summarization-japanese"}},
        "ko": {"ko": {"alias": "ml-summarization-korean"}},
    }


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "summarization"
    model_directory: Union[str, Path] = "."
    enable_metrics: bool = False
    api_version: str = "v1"
    api_key_name: str = "x-api-key"
    internal_ml_api_key: SecretStr = ""


class GlobalSettings(ServerModelSettings, Settings):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated GlobalSettings class."""
    return GlobalSettings()


settings = get_settings()
