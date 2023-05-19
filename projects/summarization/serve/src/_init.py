"""Service initialization."""

# 3rd party libraries
import requests

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import settings


logger = get_default_logger(__name__)


def init() -> None:
    """App initialization."""
    logger.debug("*" * 10)
    logger.debug("App Initialization")
    logger.info("Downloading model...")
    _setup_prompts()


def _setup_prompts() -> None:
    """Setup prompts"""
    logger.debug("+" * 10)
    logger.debug("Setup prompts")
    headers = {"x-api-key": settings.PROMPT_API_KEY}

    for lang, prompt_dict in settings.PROMPT_DICT.items():
        logger.debug(lang)
        logger.debug(prompt_dict)
        alias = prompt_dict["alias"]
        template = prompt_dict["template"]
        requests.post(
            f"{settings.PROMPT_API}/api/v1/prompts?template={template}&alias={alias}",  # noqa: E501
            headers=headers,
        )
    return
