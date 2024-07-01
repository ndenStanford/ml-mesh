"""Upload compiled model."""

# Standard Library
import os
from datetime import datetime as dt
from typing import Dict

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.base.pydantic import cast
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    CompiledNERTrackedModelCard,
    CompiledTrackedModelSettings,
    OnclusiveLogSettings,
    TrackedModelSettings,
    get_settings,
)


def upload(settings: OnclusiveBaseSettings) -> None:
    """Upload compiled model."""
    # cast settings
    tracked_model_settings = cast(settings, TrackedModelSettings)
    logging_settings = cast(settings, OnclusiveLogSettings)
    compiled_tracked_model_settings = cast(settings, CompiledTrackedModelSettings)

    logger = get_default_logger(
        name=__name__,
        fmt_level=logging_settings.fmt_level,
        level=logging_settings.level,
        json_format=logging_settings.json_format,
    )
    # --- upload compiled model
    # model directories
    base_directory: str = "./outputs"
    source_directory: str = os.path.join(base_directory, "compile")
    source_model_directory: str = os.path.join(source_directory, "model_artifacts")

    compiled_model_version = TrackedModelVersion(
        project=tracked_model_settings.project,
        api_token=tracked_model_settings.api_token.get_secret_value(),
        model=compiled_tracked_model_settings.target_model,
    )
    # model cards
    # pretrained model card
    base_model_version = TrackedModelVersion(**tracked_model_settings.model_dump())
    # get base model version assets to local disk
    base_model_card: Dict = base_model_version.download_config_from_model_version(
        neptune_attribute_path="model/model_card"
    )
    # compiled model card
    compiled_model_card = CompiledNERTrackedModelCard()
    compiled_model_version.upload_config_to_model_version(
        config=compiled_model_card.model_dump(),
        neptune_attribute_path="model/model_card",
    )
    # upload compiled ner model artifact
    compiled_model_version.upload_directory_to_model_version(
        local_directory_path=source_model_directory,
        neptune_attribute_path=compiled_model_card.model_artifact_attribute_path,
    )
    # upload test files:
    # - inputs same as trained model
    # - inference_params same as trained model
    # - predictions from compiled model, created in test workflow component
    # download model test files
    test_file_references = base_model_card["model_test_files"].keys()
    # 'inputs', 'inference_params' & 'predictions'
    for test_file_reference in test_file_references:
        compiled_model_version.upload_file_to_model_version(
            neptune_attribute_path=base_model_card["model_test_files"][
                test_file_reference
            ],
            local_file_path=os.path.join(
                base_directory, "download", test_file_reference
            ),
        )

        logger.info(
            "Successfully uploaded test file"
            f'"{os.path.join(source_directory, test_file_reference)}" into'
            f'{base_model_card["model_test_files"][test_file_reference]}'
        )
    # --- update trained model
    if base_model_version.exists("model/compiled_model_versions"):
        compiled_model_versions = base_model_version.download_config_from_model_version(
            neptune_attribute_path="model/compiled_model_versions"
        )
    else:
        compiled_model_versions = []

    compiled_model_versions.append(
        {
            "project": tracked_model_settings.project,
            "model": tracked_model_settings.model,
            "with_id": compiled_model_version._sys_id,
            "time_stamp": dt.now().strftime("%Y-%m-%d %H:%M:%s"),
        }
    )

    base_model_version.upload_config_to_model_version(
        config=compiled_model_versions,
        neptune_attribute_path="model/compiled_model_versions",
    )

    logger.info(
        f"Succesfully added new compiled model {compiled_model_version._sys_id} to the "
        f"list of compiled model versions of the trained model "
        f"{tracked_model_settings.with_id}"
    )


if __name__ == "__main__":
    upload(get_settings())
