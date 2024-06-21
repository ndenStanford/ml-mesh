"""Upload compiled model."""


# Internal libraries
from onclusiveml.core.logging import (
    OnclusiveLogMessageFormat,
    get_default_logger,
)
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    CompiledContentScoringTrackedModelCard,
    CompiledTrackedModelSpecs,
    IOSettings,
    UncompiledTrackedModelSpecs,
)


def main() -> None:
    """Upload compiled model."""
    io_settings = IOSettings()
    logger = get_default_logger(
        name=__name__,
        fmt_level=OnclusiveLogMessageFormat.DETAILED.name,
        level=io_settings.log_level,
    )
    # --- upload compiled model
    base_model_specs = UncompiledTrackedModelSpecs()
    compiled_model_specs = CompiledTrackedModelSpecs()
    compiled_model_version = TrackedModelVersion(**compiled_model_specs.model_dump())

    compiled_model_card = CompiledContentScoringTrackedModelCard()
    # upload model card - holds all settings
    compiled_model_version.upload_config_to_model_version(
        config=compiled_model_card.model_dump(),
        neptune_attribute_path="model/model_card",
    )
    # upload compiled content-scoring model artifact
    compiled_model_version.upload_file_to_model_version(
        local_file_path=io_settings.compile.compiled_model_base,
        neptune_attribute_path=compiled_model_card.model_artifact_attribute_path,
    )

    logger.info(
        f"Succesfully added new compiled model {compiled_model_version._sys_id} to the "
        f"list of compiled model versions of the uncompiled model "
        f"{base_model_specs.with_id}"
    )


if __name__ == "__main__":
    main()
