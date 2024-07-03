"""Download trained model."""

# Standard Library
import os

# Internal libraries
from onclusiveml.core.base.pydantic import OnclusiveBaseSettings
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import get_settings


settings = get_settings()


def download_model(settings: OnclusiveBaseSettings) -> None:
    """Download compiled model."""
    logger = get_default_logger(__name__)
    # model registry reference to the desired (compiled) model version
    # initialize client for specific model version
    mv = TrackedModelVersion(
        with_id=settings.with_id,
        mode=settings.mode,
        api_token=settings.api_token.get_secret_value(),
        project=settings.project,
    )

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
    download_model(settings)
