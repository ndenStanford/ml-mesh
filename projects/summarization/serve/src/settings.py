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
    PROMPT_API: str = "https://internal.api.ml.dev.onclusive.org"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "1234"
    SUMMARIZATION_DEFAULT_MODEL: str = "gpt-4-1106-preview"

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


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated Settings class."""
    return Settings()


settings = get_settings()
