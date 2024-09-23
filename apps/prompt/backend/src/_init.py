"""Service initialization."""

# Standard Library
import logging
from typing import List, Type

# 3rd party libraries
from botocore.exceptions import ClientError
from dyntastic import Dyntastic

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.core.system import SystemInfo

# Source
from src.model.constants import DEFAULT_MODELS
from src.model.tables import LanguageModel
from src.project.tables import Project
from src.prompt.tables import PromptTemplate
from src.settings import get_settings


settings = get_settings()


logger = get_default_logger(__name__)


def init() -> None:
    """App initialization."""
    logger.info("Creating tables...")
    _create_tables([LanguageModel, PromptTemplate, Project])
    _initialize_table(LanguageModel, DEFAULT_MODELS)

    if SystemInfo.in_docker():
        _syncronize_prompts()


def _create_tables(tables: List[Type[Dyntastic]]) -> None:
    """Create Tables."""
    for table in tables:
        try:
            table.create_table()
        except ClientError:
            logging.info("Table already exists, skipping creation ...")


def _initialize_table(table: Type[Dyntastic], values: List[dict]) -> None:
    """Initializes table."""
    for value in values:
        row = table.safe_get(value["alias"])
        if row is None:
            table(**value).save()
