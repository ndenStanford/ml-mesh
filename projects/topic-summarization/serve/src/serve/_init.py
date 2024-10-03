# isort: skip_file
# Standard Library
from typing import Type

# 3rd party libraries
from botocore.exceptions import ClientError
from dyntastic import Dyntastic, Index

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.serve.tables import TopicSummaryDynamoDB
from src.settings import get_settings


logger = get_default_logger(__name__)
settings = get_settings()


def init() -> None:
    """App initialization."""
    logger.info("Creating tables...")
    _create_table(TopicSummaryDynamoDB)


def _create_table(table: Type[Dyntastic]) -> None:
    """Create Tables."""
    try:
        timestamp_index = Index(
            hash_key="timestamp_date",
            index_name="timestamp_date-index",
        )
        table.create_table(timestamp_index)
    except ClientError as e:
        logger.info("Table creation failed with error: {}".format(e))
