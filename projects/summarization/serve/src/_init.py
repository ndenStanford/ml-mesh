"""Service initialization."""

# 3rd party libraries
import requests

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import settings  # type: ignore[attr-defined]


logger = get_default_logger(__name__)


def init() -> None:
    """App initialization."""
    logger.info("Setting up prompts...")
