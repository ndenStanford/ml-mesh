"""Settings."""

# Standard Library
from typing import Optional

# 3rd party libraries
from pydantic import BaseSettings


class Settings(BaseSettings):
    """API configuration."""

    # Generic settings

    # api name
    API_NAME: str = "Entity Linking"

    # api description
    API_DESCRIPTION: str = ""

    # api environment
    ENVIRONMENT: str = "stage"

    # api debug level
    DEBUG: bool = True

    # api runtime
    KUBERNETES_IN_POD: bool = False

    # log level
    LOGGING_LEVEL: str = "info"

    # documentation endpoint
    DOCS_URL: Optional[str] = None

    # entity fishing endpoint
    # our endpoint does not have load balancer for now
    ENTITY_FISHING_ENDPOINT: str = (
        "https://internal.api.ml.stage.onclusive.com/service/disambiguate"
    )

    # entity recognition endpoint
    ENTITY_RECOGNITION_ENDPOINT: str = (
        "https://eks-data-prod.onclusive.com/predictions/ner_neuron_v2"
    )

    API_KEY_NAME: str = "x-api-key"
    INTERNAL_ML_ENDPOINT_API_KEY: str


settings = Settings()
