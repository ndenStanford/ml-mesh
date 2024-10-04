"""Downlad trained model."""

# Standard Library
import os
from typing import Dict

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.base.pydantic import cast
from onclusiveml.core.logging import OnclusiveLogSettings, get_default_logger
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import TrackedModelSettings, get_settings


def download(settings: OnclusiveBaseSettings) -> None:
    """Downlad trained model."""
    # cast settings
    tracked_model_settings = cast(settings, TrackedModelSettings)
    logging_settings = cast(settings, OnclusiveLogSettings)

    logger = get_default_logger(
        name=__name__,
        fmt_level=logging_settings.fmt_level,
        level=logging_settings.level,
        json_format=logging_settings.json_format,
    )
    # model directory
    target_directory: str = os.path.join("./outputs", "download")
    target_model_directory: str = os.path.join(target_directory, "model_artifacts")
    # get read-only base model version
    base_model_version = TrackedModelVersion(**tracked_model_settings.model_dump())
    # get base model version assets to local disk
    base_model_card: Dict = base_model_version.download_config_from_model_version(
        neptune_attribute_path="model/model_card"
    )
    # download model artifact
    base_model_version.download_directory_from_model_version(
        local_directory_path=target_model_directory,
        neptune_attribute_path=base_model_card["model_artifact_attribute_path"],
    )

    logger.info(
        f"Successfully downloaded uncompiled ner model into "
        f"{target_model_directory}"
    )
    # download model test files
    test_file_references = base_model_card["model_test_files"].keys()
    # 'inputs', 'inference_params' & 'predictions'
    for test_file_reference in test_file_references:
        base_model_version.download_file_from_model_version(
            neptune_attribute_path=base_model_card["model_test_files"][
                test_file_reference
            ],
            local_file_path=os.path.join(target_directory, test_file_reference),
        )

        logger.info(
            f'Successfully downloaded test file "{test_file_reference}" into '
            f"{os.path.join(target_directory, test_file_reference)}"
        )

    base_model_version.stop()


if __name__ == "__main__":
    download(get_settings())
