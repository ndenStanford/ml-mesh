"""Compile model."""

# Standard Library
from typing import Dict

# ML libs
from transformers import pipeline

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.core.logging import (
    OnclusiveLogMessageFormat,
    get_default_logger,
)
from onclusiveml.models.sentiment import CompiledSent
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    IOSettings,
    SentPipelineCompilationSettings,
    UncompiledTrackedModelSpecs,
)


def compile_model() -> None:
    """Compile model."""
    io_settings = IOSettings()
    logger = get_default_logger(
        name=__name__,
        fmt_level=OnclusiveLogMessageFormat.DETAILED.name,
        level=io_settings.log_level,
    )
    # get read-only base model version
    base_model_specs = UncompiledTrackedModelSpecs()
    base_model_version = TrackedModelVersion(**base_model_specs.model_dump())
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
    # compile base model pipeline for sent
    sent_pipeline_compilation_settings = SentPipelineCompilationSettings()
    logger.debug(
        f"Using the following sent pipeline compilation settings: "
        f"{sent_pipeline_compilation_settings.model_dump()}. Compiling ..."
    )

    compiled_sent_pipeline = CompiledPipeline.from_pipeline(
        pipeline=base_model_pipeline,
        **sent_pipeline_compilation_settings.model_dump(exclude={"pipeline_name"}),
    )

    compiled_sent = CompiledSent(compiled_sent_pipeline)
    # export compiled sent model for next workflow component: test
    compiled_sent.save_pretrained(io_settings.compile.model_directory)

    logger.info(
        f"Successfully exported compiled sent model to {io_settings.compile.model_directory}"
    )


if __name__ == "__main__":
    compile_model()
