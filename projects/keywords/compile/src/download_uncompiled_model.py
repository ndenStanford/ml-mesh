# Standard Library
from typing import Dict

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    IOSettings,
    UncompiledTrackedModelSpecs,
)


def main() -> None:

    io_settings = IOSettings()
    logger = get_default_logger(
        name=__name__, fmt=LogFormat.DETAILED.value, level=io_settings.log_level
    )
    # get read-only base model version
    base_model_specs = UncompiledTrackedModelSpecs()
    base_model_version = TrackedModelVersion(**base_model_specs.dict())
    # get base model version assets to local disk
    base_model_card: Dict = base_model_version.download_config_from_model_version(
        neptune_attribute_path="model/model_card"
    )
    # download model artifact
    base_model_version.download_directory_from_model_version(
        local_directory_path=io_settings.download.model_directory,
        neptune_attribute_path=base_model_card["model_artifact_attribute_path"],
    )

    logger.info(
        f"Successfully downloaded uncompiled keybert model into "
        f"{io_settings.download.model_directory}"
    )
    # download model test files
    test_file_references = base_model_card["model_test_files"].keys()
    # 'inputs', 'inference_params' & 'predictions'
    for test_file_reference in test_file_references:
        base_model_version.download_file_from_model_version(
            neptune_attribute_path=base_model_card["model_test_files"][
                test_file_reference
            ],
            local_file_path=io_settings.download.test_files[test_file_reference],
        )

        logger.info(
            f'Successfully downloaded test file "{test_file_reference}" into '
            f"{io_settings.download.test_files[test_file_reference]}"
        )

    base_model_version.stop()


if __name__ == "__main__":
    main()
