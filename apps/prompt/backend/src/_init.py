"""Service initialization."""

# Standard Library
from typing import List

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.db import BaseTable
from src.model.schemas import ModelSchema
from src.model.tables import ModelTable
from src.prompt.schemas import PromptTemplateSchema
from src.prompt.tables import PromptTemplateTable
from src.settings import get_settings


settings = get_settings()


logger = get_default_logger(__name__)


def init() -> None:
    """App initialization."""
    logger.info("Creating tables...")
    _create_tables([PromptTemplateTable, ModelTable])
    fill_model_table()
    fill_prompt_table()


def fill_model_table() -> None:
    """Model filling."""
    logger.info("Adding models to model table...")
    list_of_models = []
    models = ModelSchema.get()

    # make list of predefined model names from database
    for x in models:
        list_of_models.append(x.model_name)

    # Saving predifined models into database
    # If model id doesn't exist, then add model to table
    for _, model in settings.LIST_OF_MODELS.items():
        if model[0] in list_of_models:
            continue
        logger.debug("Adding model: {}".format(model[0]))
        model = ModelSchema(model_name=model[0], parameters=model[1])
        model.save()


def fill_prompt_table() -> None:
    """Prompts filling."""
    logger.info("Adding prompts to prompts table...")
    list_of_prompts = settings.LIST_OF_PROMPTS
    prompts = PromptTemplateSchema.get()
    list_of_aliases = []

    # make list of predefined aliases from database
    for x in prompts:
        list_of_aliases.append(x.alias)

    # Saving predifined prompts into database
    # If prompt doesn't exist, then add prompt to table
    for _, prompt in list_of_prompts.items():
        if prompt[1] in list_of_aliases:
            continue
        logger.debug("Adding prompt: {}".format(prompt[0]))
        prompt = PromptTemplateSchema(template=prompt[0], alias=prompt[1])
        prompt.save()


def _create_tables(tables: List[BaseTable]) -> None:
    """Create Tables."""
    for table in tables:
        if not table.exists():
            table.create_table(read_capacity_units=3, write_capacity_units=3, wait=True)
