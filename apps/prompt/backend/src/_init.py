"""Service initialization."""

# Standard Library
from typing import List

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.db import BaseTable
from src.model.tables import ModelTable
from src.prompt.tables import PromptTemplateTable
from src.model._init import fill_table

logger = get_default_logger(__name__)


def init() -> None:
    """App initialization."""
    logger.info("Creating tables...")
    _create_tables([PromptTemplateTable, ModelTable])
    fill_table()


def _create_tables(tables: List[BaseTable]) -> None:
    """Create Tables."""
    for table in tables:
        if not table.exists():
            table.create_table(read_capacity_units=3, write_capacity_units=3, wait=True)
