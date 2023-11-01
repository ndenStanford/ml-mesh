"""Service initialization."""
# isort: skip_file

# 3rd party libraries
import requests

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.serve.settings import Settings

logger = get_default_logger(__name__)

settings = Settings()


def init() -> None:
    """App initialization."""
    logger.info("Setting up prompts...")
    _setup_prompts()


def _setup_prompts() -> None:
    """Setup prompts."""
    headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

    for prompt_key in settings.PROMPT_DICT.keys():
        alias = settings.PROMPT_DICT[prompt_key]["alias"]
        template = settings.PROMPT_DICT[prompt_key]["template"]
        requests.post(
            f"{settings.PROMPT_API}/api/v1/prompts?template={template}&alias={alias}",  # noqa: E501
            headers=headers,
        )
    return
