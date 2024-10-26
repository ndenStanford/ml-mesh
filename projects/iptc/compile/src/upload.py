"""Upload compiled model."""

# Standard Library
from datetime import datetime as dt

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
    """Upload compiled model."""
    logger = get_default_logger(__name__)
    # model registry reference to the desired (compiled) model version
    # initialize client for specific model version
    # --- upload compiled model
    compiled_model_version = TrackedModelVersion(
        model=settings.compiled_model,
        api_token=settings.api_token.get_secret_value(),
        project=settings.project,
    )

    compiled_model_version.upload_config_to_model_version(
        config=settings.model_card.model_dump(exclude={"api_token"}),
        neptune_attribute_path="model/model_card",
    )
    # upload compiled iptc model artifact
    compiled_model_version.upload_directory_to_model_version(
        local_directory_path=settings.model_directory(CompileWorkflowTasks.COMPILE),
        neptune_attribute_path=settings.model_card.model_artifact_attribute_path,
    )
    # upload test files:
    # - inputs same as uncompiled model
    # - inference_params same as uncompiled model
    # - predictions from compiled model, created in test workflow component
    compiled_model_version.upload_file_to_model_version(
        neptune_attribute_path=settings.model_card.model_test_files.inputs,
        local_file_path=settings.test_files(CompileWorkflowTasks.DOWNLOAD)["inputs"],
    )

    compiled_model_version.upload_file_to_model_version(
        neptune_attribute_path=settings.model_card.model_test_files.inference_params,
        local_file_path=settings.test_files(CompileWorkflowTasks.DOWNLOAD)[
            "inference_params"
        ],
    )

    compiled_model_version.upload_file_to_model_version(
        neptune_attribute_path=settings.model_card.model_test_files.predictions,
        local_file_path=settings.test_files(CompileWorkflowTasks.TEST)["predictions"],
    )
    # --- update trained model
    # get read-only base model version
    trained_model_version = TrackedModelVersion(
        with_id=settings.with_id,
        # mode=settings.mode,
        api_token=settings.api_token.get_secret_value(),
        project=settings.project,
    )

    if trained_model_version.exists("model/compiled_model_versions"):
        compiled_model_versions = (
            trained_model_version.download_config_from_model_version(
                neptune_attribute_path="model/compiled_model_versions"
            )
        )
    else:
        compiled_model_versions = []

    compiled_model_versions.append(
        {
            "project": settings.project,
            "model": settings.compiled_model,
            "with_id": compiled_model_version._sys_id,
            "time_stamp": dt.now().strftime("%Y-%m-%d %H:%M:%s"),
        }
    )

    trained_model_version.upload_config_to_model_version(
        config=compiled_model_versions,
        neptune_attribute_path="model/compiled_model_versions",
    )

    logger.info(
        f"Succesfully added new compiled model {compiled_model_version._sys_id} to the "
        f"list of compiled model versions of the uncompiled model "
        f"{settings.with_id}"
    )


if __name__ == "__main__":
    settings = get_settings()
    init_logging(cast(settings, OnclusiveLogSettings))
    main(settings)
