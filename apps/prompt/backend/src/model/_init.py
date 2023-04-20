"""Model table filling."""

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.model.schemas import ModelSchema
from src.settings import get_settings


settings = get_settings()

logger = get_default_logger(__name__)


def fill_table() -> None:
    """Model filling."""
    logger.info("Adding models to model table...")
    list_of_models = settings.LIST_OF_MODELS

    # Saving predifined models into database
    # If model id doesn't exist, then add model to table
    for id, model in list_of_models.items():
        try:
            _ = ModelSchema.get(id)
        except Exception as e:
            logger.debug(e)
            logger.debug("Adding model: {}".format(model[0]))
            model = ModelSchema(id=id, model_name=model[0], parameters=model[1])
            model.save()
