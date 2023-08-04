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
    logger.info("Setting up prompts...")
    _setup_prompts()


def _setup_prompts() -> None:
    """Setup prompts"""
    headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

    for input_lang, target_lang_dict in settings.PROMPT_DICT.items():
        for target_lang, prompt_dict in target_lang_dict.items():
            alias = prompt_dict["alias"]
            template = prompt_dict["template"]
            requests.post(
                f"{settings.PROMPT_API}/api/v1/prompts?template={template}&alias={alias}",  # noqa: E501
                headers=headers,
            )
    return
