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
    ENTITY_FISHING_ENDPOINT: str = 'https://cloud.science-miner.com/nerd/service/disambiguate' # our endpoint does not have load balancer for now

    # entity recognition endpoint
    ENTITY_RECOGNITION_ENDPOINT: str = 'https://eks-data-prod.onclusive.com/predictions/ner_neuron_v2'



settings = Settings()
