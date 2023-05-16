"""Settings."""

# Standard Library
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
    ENVIRONMENT: str = "stage"

    # Debug level
    DEBUG: bool = True

    # API runtime
    KUBERNETES_IN_POD: bool = False

    # Logging level
    LOGGING_LEVEL: str = "info"

    # documentation endpoint
    DOCS_URL: Optional[str] = None

    # OpenAI api key
    OPENAI_API_KEY: str = ""

    # Prompt url
    PROMPT_API: str = "http://0.0.0.0:4000"
    PROMPT_API_KEY: str = "1234"

    ENGLISH_SUMMARIZATION_ALIAS = "english-summarization-prompt"

settings = Settings()