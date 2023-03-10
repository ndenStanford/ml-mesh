"""Service initialization."""

from src.settings import settings
from onclusiveml.core.logger import get_default_logger

from fastapi import FastAPI
from keybert import KeyBERT


logger = get_default_logger(__name__)


def init(app: FastAPI) -> None:
    """App initialization."""
    logger.info("Downloading model...")
    _load_models()
    return app


def _load_models():
    """Load models."""
    _ = KeyBERT(settings.MODEL_NAME)
