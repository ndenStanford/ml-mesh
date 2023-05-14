"""Service initialization."""
import requests

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import settings


logger = get_default_logger(__name__)


def init() -> None:
    """App initialization."""
    logger.info("Downloading model...")
    _setup_prompts()


def _setup_prompts() -> None:
    """Setup prompts"""
    headers = {'x-api-key': settings.PROMPT_API_KEY}
    english_summarization_template = ("Give an abstractive summary while retaining important quotes of speech in less than " 
            + str(100)  # noqa: W503 
            + " words: "  # noqa: W503
            + "\n"  # noqa: W503
            + "{content}"  # noqa: W503
            + "\n"  # noqa: W503
    )
    english_summarization_alias = settings.ENGLISH_SUMMARIZATION_ALIAS
    requests.post(f"{settings.PROMPT_API}/api/v1/prompts?template={english_summarization_template}&alias={english_summarization_alias}", headers = headers)
    return
