# isort: skip_file

# 3rd party libraries
from botocore.exceptions import ClientError
from dyntastic import Index

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.serve.tables import TopicSummaryDynamoDB, TopicSummaryResponseDB
from src.settings import get_settings


logger = get_default_logger(__name__)
settings = get_settings()


def init() -> None:
    """App initialization."""
    logger.info("Creating tables...")
    _create_tables()


def _create_tables() -> None:
    """Create Tables."""
    try:
        timestamp_index = Index(
            hash_key="timestamp_date",
            index_name="timestamp_date-index",
        )
        TopicSummaryDynamoDB.create_table(timestamp_index)
    except ClientError as e:
        logger.info("Table creation failed with error: {}".format(e))

    try:
        TopicSummaryResponseDB.create_table()
    except ClientError as e:
        logger.info("Table creation failed with error: {}".format(e))
