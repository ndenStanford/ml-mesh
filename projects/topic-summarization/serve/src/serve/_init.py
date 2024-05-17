# Standard Library
from typing import Type

# 3rd party libraries
from botocore.exceptions import ClientError
from dyntastic import Dyntastic

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.serve.tables import TopicSummaryDynamoDB

logger = get_default_logger(__name__)


def init() -> None:
    """App initialization."""
    logger.info("Creating tables...")
    _create_table(TopicSummaryDynamoDB)


def _create_table(table: Type[Dyntastic]) -> None:
    """Create Tables."""
    try:
        table.create_table()
    except ClientError as e:
        logger.info("Table creation failed with error: {}".format(e))
