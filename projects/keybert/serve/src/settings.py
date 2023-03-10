"""Settings."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """API configuration."""

    # Generic settings
    API_NAME: str = "Keybert Prediction"
    API_DESCRIPTION: str = ""
    ENVIRONMENT: str = "stage"
    DEBUG: bool = True
    KUBERNETES_IN_POD: bool = False
    LOGGING_LEVEL: str = "info"

    # Keybert settings
    MODEL_NAME: str = "paraphrase-multilingual-MiniLM-L12-v2"


settings = Settings()
