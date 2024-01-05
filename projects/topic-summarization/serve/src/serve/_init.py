"""Service initialization."""
# isort: skip_file

# Standard Library
from typing import Optional

# 3rd party libraries
# import requests
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.serve.category_storage import Category_list

logger = get_default_logger(__name__)


class Settings(BaseSettings):
    """API configuration."""

    API_NAME: str = "Topic detection"
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
    DOCS_URL: Optional[str] = "/topic-detection/docs"
    OPENAPI_URL: Optional[str] = "/topic-detection/openapi.json"
    # OpenAI api key
    OPENAI_API_KEY: str = ""
    # Prompt url
    PROMPT_API: str = "http://prompt-backend:4000"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "1234"
    # interested aspects/categories
    CATEGORY_LIST = Category_list


settings = Settings()
