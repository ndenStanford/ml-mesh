"""Model table filling."""

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.model.schemas import ModelSchema
from src.settings import get_settings


settings = get_settings()

logger = get_default_logger(__name__)

list_of_models = settings.LIST_OF_MODELS


def fill_table() -> None:
    """Model filling."""
    logger.info("Adding models to model table...")
    for model_name in list_of_models:
        model = ModelSchema(model_name=model_name)
        model.save()
