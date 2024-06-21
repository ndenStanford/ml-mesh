"""Download trained model."""

# Standard Library
from typing import Dict

# Internal libraries
from onclusiveml.core.logging import (
    OnclusiveLogMessageFormat,
    get_default_logger,
)
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    IOSettings,
    UncompiledTrackedModelSpecs,
)


def download_uncompiled_model() -> None:
    """Download trained model."""
    io_settings = IOSettings()
    logger = get_default_logger(
        name=__name__,
        fmt_level=OnclusiveLogMessageFormat.DETAILED.name,
        level=io_settings.log_level,
    )
    # get read-only base model version
    base_model_specs = UncompiledTrackedModelSpecs()
    base_model_version = TrackedModelVersion(**base_model_specs.model_dump())
    # get base model version assets to local disk
    base_model_card: Dict = base_model_version.download_config_from_model_version(
        neptune_attribute_path="model/model_card"
    )
    # download model artifact
    base_model_version.download_file_from_model_version(
        local_file_path=io_settings.download.model_base,
        neptune_attribute_path=base_model_card["model_artifact_attribute_path"],
    )

    logger.info(
        f"Successfully downloaded uncompiled content-scoring model into "
        f"{io_settings.download.model_base}"
    )

    base_model_version.stop()


if __name__ == "__main__":
    download_uncompiled_model()
