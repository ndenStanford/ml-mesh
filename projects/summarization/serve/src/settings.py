"""Settings."""

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

    # OpenAI api key
    OPENAI_API_KEY: str


settings = Settings()
