"""Compile model."""

# Standard Library
from typing import Dict

# ML libs
from transformers import pipeline

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.iptc import CompiledIPTC
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    IOSettings,
    IPTCPipelineCompilationSettings,
    UncompiledTrackedModelSpecs,
)


def main() -> None:
    """Compile model."""
    io_settings = IOSettings()
    logger = get_default_logger(
        name=__name__, fmt=LogFormat.DETAILED.value, level=io_settings.log_level
    )
    # get read-only base model version
    base_model_specs = UncompiledTrackedModelSpecs()
    base_model_version = TrackedModelVersion(**base_model_specs.dict())
    # get base model card
    base_model_card: Dict = base_model_version.download_config_from_model_version(
        "model/model_card"
    )

    logger.debug(f"Base model model_card: {base_model_card}")

    # re-load base model pipeline
    base_model_pipeline = pipeline(
        task=base_model_card["model_params"]["huggingface_pipeline_task"],
        model=io_settings.download.model_directory,
    )
    # compile base model pipeline for iptc
    iptc_pipeline_compilation_settings = IPTCPipelineCompilationSettings()

    logger.debug(
        f"Using the following iptc pipeline compilation settings: "
        f"{iptc_pipeline_compilation_settings.dict()}. Compiling ..."
    )

    compiled_iptc_pipeline = CompiledPipeline.from_pipeline(
        pipeline=base_model_pipeline,
        **iptc_pipeline_compilation_settings.dict(exclude={"pipeline_name"}),
    )

    compiled_iptc = CompiledIPTC(compiled_iptc_pipeline)
    # export compiled iptc model for next workflow component: test
    compiled_iptc.save_pretrained(io_settings.compile.model_directory)

    logger.debug(
        f"Successfully exported compiled iptc model to {io_settings.compile.model_directory}"
    )


if __name__ == "__main__":
    main()
