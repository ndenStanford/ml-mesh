"""Service initialization."""
# ML libs

# ML libs
from keybert import KeyBERT

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import settings


logger = get_default_logger(__name__)


def init() -> None:
    """App initialization."""
    logger.info("Downloading model...")
    _load_models()


def _load_models() -> None:
    """Load models."""
    _ = KeyBERT(settings.MODEL_NAME)
