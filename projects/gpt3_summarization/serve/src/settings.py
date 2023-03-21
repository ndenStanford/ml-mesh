"""Settings."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """API configuration."""

    # Generic settings
    API_NAME: str = "GPT3 Summarization Prediction"
    API_DESCRIPTION: str = ""
    ENVIRONMENT: str = "stage"
    DEBUG: bool = True
    KUBERNETES_IN_POD: bool = False
    LOGGING_LEVEL: str = "info"
    OPENAI_API_KEY: str


settings = Settings()
