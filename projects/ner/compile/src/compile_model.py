"""Compile model."""

# Standard Library
from typing import Dict

# ML libs
from transformers import pipeline

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.ner import CompiledNER
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    CompilePipelineIOSettings,
    NERPipelineCompilationSettings,
    UncompiledTrackedModelSpecs,
)


def compile_model(
    io_settings: CompilePipelineIOSettings,
    base_model_specs: UncompiledTrackedModelSpecs,
    ner_pipeline_compilation_settings: NERPipelineCompilationSettings,
) -> None:
    """Compile model."""
    logger = get_default_logger(
        name=__name__, fmt=LogFormat.DETAILED.value, level=io_settings.logger_level
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
    # compile base model pipeline for NER

    logger.debug(
        f"Using the following ner pipeline compilation settings: "
        f"{ner_pipeline_compilation_settings.dict()}. Compiling ..."
    )

    compiled_ner_pipeline = CompiledPipeline.from_pipeline(
        pipeline=base_model_pipeline,
        **ner_pipeline_compilation_settings.dict(exclude={"pipeline_name"}),
    )

    compiled_ner = CompiledNER(compiled_ner_pipeline)
    # export compiled ner model for next workflow component: test
    compiled_ner.save_pretrained(io_settings.compile.model_directory)

    logger.info(
        f"Successfully exported compiled ner model to {io_settings.compile.model_directory}"
    )
