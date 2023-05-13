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
    english_summarization_template = "{content} Summarize the article in 20 words"
    english_summarization_alias = "english_summarization_prompt"
    q = requests.post(f"{settings.PROMPT_API}/api/v1/prompts?template={english_summarization_template}&alias={english_summarization_alias}", headers = headers)
