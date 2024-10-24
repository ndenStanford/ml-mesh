"""Download compiled model."""

# Standard Library
import os
import boto3

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.base.pydantic import cast
from onclusiveml.core.logging import (
    OnclusiveLogSettings,
    get_default_logger,
    init_logging,
)
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import get_settings


settings = get_settings()


def download_model(settings: OnclusiveBaseSettings) -> None:
    """Download compiled model."""
    logger = get_default_logger(__name__)
    # model registry reference to the desired (compiled) model version
    # initialize client for specific model version

    try:
        session = boto3.Session()
        current_region = session.region_name

        # Print the current AWS region
        print(f"Current AWS region: {current_region}")

        # Create an S3 client
        s3_client = session.client('s3')

        # List all S3 buckets
        response = s3_client.list_buckets()

        # Print bucket names
        print("Available S3 buckets:")
        for bucket in response['Buckets']:
            print(f"- {bucket['Name']}")
    except Exception as e:
        print('=======================error', e)

    mv = TrackedModelVersion(
        with_id=settings.with_id,
        mode=settings.mode,
        api_token=settings.api_token.get_secret_value(),
        project=settings.project,
    )

    if not os.path.isdir(settings.model_directory):
        # if the target dir does not exist, download all model artifacts for the model version to
        # local
        logger.info(f"settings.model_directory: {settings.model_directory}")
        mv.download_directory_from_model_version(
            local_directory_path=settings.model_directory,
            neptune_attribute_path="model",
        )
    elif not os.listdir(settings.model_directory):
        # if the target dir does exist but is empty, download all model artifacts for the model
        # version to local
        mv.download_directory_from_model_version(
            local_directory_path=settings.model_directory,
            neptune_attribute_path="model",
        )
    else:
        logger.info(
            f"The specified output directory {settings.model_directory} already "
            f"exists and is not empty: {os.listdir(settings.model_directory)}. Model "
            "download skipped."
        )
    # shutdown client
    mv.stop()


if __name__ == "__main__":
    init_logging(cast(settings, OnclusiveLogSettings))
    download_model(settings)
