"""Download trained model."""

# Standard Library
from typing import Dict

# Internal libraries
from onclusiveml.compile.constants import CompileWorkflowTasks
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


def main(settings: OnclusiveBaseSettings) -> None:
    """Download trained model."""
    logger = get_default_logger(__name__)
    # model registry reference to the desired (compiled) model version
    # initialize client for specific model version
    model_version = TrackedModelVersion(
        with_id=settings.with_id,
        api_token=settings.api_token.get_secret_value(),
        project=settings.project,
    )
    # get model card
    model_card: Dict = model_version.download_config_from_model_version(
        "model/model_card"
    )
    # download model artifact
    model_version.download_directory_from_model_version(
        local_directory_path=settings.model_directory(CompileWorkflowTasks.DOWNLOAD),
        neptune_attribute_path=model_card["model_artifact_attribute_path"],
    )

    logger.info(
        f"Successfully downloaded trained iptc model into "
        f"{settings.model_directory(CompileWorkflowTasks.DOWNLOAD)}"
    )
    # download model test files
    test_file_references = model_card["model_test_files"].keys()
    # 'inputs', 'inference_params' & 'predictions'
    for test_file_reference in test_file_references:
        model_version.download_file_from_model_version(
            neptune_attribute_path=model_card["model_test_files"][test_file_reference],
            local_file_path=settings.test_files(CompileWorkflowTasks.DOWNLOAD)[
                test_file_reference
            ],
        )

        logger.info(
            f'Successfully downloaded test file "{test_file_reference}" into '
            f"{settings.test_files(CompileWorkflowTasks.DOWNLOAD)[test_file_reference]}"
        )

    model_version.stop()


if __name__ == "__main__":
    settings = get_settings()
    init_logging(cast(settings, OnclusiveLogSettings))
    main(settings)
