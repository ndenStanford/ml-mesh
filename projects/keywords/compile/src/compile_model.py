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
from onclusiveml.models.keywords import CompiledKeyBERT
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    DocumentPipelineCompilationSettings,
    IOSettings,
    UncompiledTrackedModelSpecs,
    WordPipelineCompilationSettings,
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
    # compile base model pipeline for word embedding feature extraction
    word_pipeline_compilation_settings = WordPipelineCompilationSettings()
    logger.debug(
        f"Using the following word pipeline compilation settings: "
        f"{word_pipeline_compilation_settings.dict()}. Compiling ..."
    )

    compiled_word_embedding_pipeline = CompiledPipeline.from_pipeline(
        pipeline=base_model_pipeline,
        **word_pipeline_compilation_settings.dict(exclude={"pipeline_name"}),
    )
    # compile base model pipeline for document embedding feature extraction
    document_pipeline_compilation_settings = DocumentPipelineCompilationSettings()
    logger.debug(
        f"Using the following document pipeline compilation settings: "
        f"{document_pipeline_compilation_settings.dict()}. Compiling ..."
    )

    compiled_document_embedding_pipeline = CompiledPipeline.from_pipeline(
        pipeline=base_model_pipeline,
        **document_pipeline_compilation_settings.dict(exclude={"pipeline_name"}),
    )
    # assemble compiled keybert model
    compiled_keybert = CompiledKeyBERT(
        document_pipeline=compiled_document_embedding_pipeline,
        compiled_word_pipeline=compiled_word_embedding_pipeline,
    )
    # export compiled keybert model for next workflow component: test
    compiled_keybert.save_pretrained(io_settings.compile.model_directory)

    logger.info(
        f"Successfully exported compiled keybert model to {io_settings.compile.model_directory}"
    )


if __name__ == "__main__":
    compile_model()
