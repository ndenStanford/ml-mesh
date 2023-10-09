"""Download knowledge graph."""

# 3rd party libraries
import boto3
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.download.s3 import sync_folder
from src.settings import get_settings


settings = get_settings()


def main(settings: BaseSettings) -> None:
    """Download compiled model."""
    logger = get_default_logger(__name__)

    logger.debug("Syncing knowledge bases ....")
    # download knowledge base
    for kb in settings.knowledge_bases:
        logger.debug(f"Syncing knowledge base: {kb}....")
        sync_folder(
            client=boto3.client("s3"),
            bucket=settings.source_bucket,
            source_folder=f"entity-fishing/0.0.6/db/db-{kb}",
            target_folder=f"/opt/entity-fishing/data/db/db-{kb}",
        )


if __name__ == "__main__":
    main(settings)
