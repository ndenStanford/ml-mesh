"""Upload compiled model."""
# Standard Library
from datetime import datetime as dt

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    CompiledKeywordsTrackedModelCard,
    CompiledTrackedModelSpecs,
    IOSettings,
    UncompiledTrackedModelSpecs,
)


def upload_compiled_model(
    io_settings: IOSettings,
    base_model_specs: UncompiledTrackedModelSpecs,
    compiled_model_specs: CompiledTrackedModelSpecs,
    compiled_model_card: CompiledKeywordsTrackedModelCard,
) -> None:
    """Upload compiled model."""
    logger = get_default_logger(
        name=__name__, fmt=LogFormat.DETAILED.value, level=io_settings.log_level
    )

    # --- upload compiled model
    compiled_model_version = TrackedModelVersion(**compiled_model_specs.dict())

    # upload model card - holds all settings
    compiled_model_version.upload_config_to_model_version(
        config=compiled_model_card.dict(), neptune_attribute_path="model/model_card"
    )
    # upload compiled keybert model artifact
    compiled_model_version.upload_directory_to_model_version(
        local_directory_path=io_settings.compile.model_directory,
        neptune_attribute_path=compiled_model_card.model_artifact_attribute_path,
    )
    # upload test files:
    # - inputs same as uncompiled model
    # - inference_params same as uncompiled model
    # - predictions from compiled model, created in test workflow component
    compiled_model_version.upload_file_to_model_version(
        neptune_attribute_path=compiled_model_card.model_test_files.inputs,
        local_file_path=io_settings.download.test_files["inputs"],
    )

    compiled_model_version.upload_file_to_model_version(
        neptune_attribute_path=compiled_model_card.model_test_files.inference_params,
        local_file_path=io_settings.download.test_files["inference_params"],
    )

    compiled_model_version.upload_file_to_model_version(
        neptune_attribute_path=compiled_model_card.model_test_files.predictions,
        local_file_path=io_settings.test.test_files["predictions"],
    )
    # --- update uncompiled model
    # get read-only base model version
    base_model_version = TrackedModelVersion(**base_model_specs.dict())

    if base_model_version.exists("model/compiled_model_versions"):
        compiled_model_versions = base_model_version.download_config_from_model_version(
            neptune_attribute_path="model/compiled_model_versions"
        )
    else:
        compiled_model_versions = []

    compiled_model_versions.append(
        {
            "project": compiled_model_specs.project,
            "model": compiled_model_specs.model,
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
        f"list of compiled model versions of the uncompiled model "
        f"{base_model_specs.with_id}"
    )
