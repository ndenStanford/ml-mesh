"""Download compiled model."""

# Standard Library
import os

# 3rd party libraries
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import get_settings


settings = get_settings()


def main(settings: BaseSettings) -> None:
    """Download compiled model."""
    logger = get_default_logger(__name__)
    # model registry reference to the desired (compiled) model version
    # initialize client for specific model version
    mv = TrackedModelVersion(with_id=settings.with_id, mode=settings.mode)

    if not os.path.isdir(settings.model_directory):
        # if the target dir does not exist, download all model artifacts for the model version to
        # local
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
    main(settings)
