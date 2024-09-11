"""Compile model."""

# Standard Library
from typing import Dict

# ML libs
from transformers import pipeline

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.compile.constants import CompileWorkflowTasks
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.base.pydantic import cast
from onclusiveml.core.logging import (
    OnclusiveLogSettings,
    get_default_logger,
    init_logging,
)
from onclusiveml.models.keywords import CompiledKeyBERT
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import PipelineCompilationSettings, get_settings


def main(settings: OnclusiveBaseSettings) -> None:
    """Compile model."""
    logger = get_default_logger(__name__)
    # get read-only base model version
    model_version = TrackedModelVersion(
        with_id=settings.with_id,
        mode=settings.mode,
        api_token=settings.api_token.get_secret_value(),
        project=settings.project,
    )
    # get base model card
    model_card: Dict = model_version.download_config_from_model_version(
        "model/model_card"
    )

    logger.debug(f"Model card: {model_card}")
    # re-load base model pipeline

    base_model_pipeline = pipeline(
        task=model_card["model_params"]["huggingface_pipeline_task"],
        model=settings.model_directory(CompileWorkflowTasks.DOWNLOAD),
    )

    logger.debug(
        f"Using the following pipeline compilation settings: "
        f"{cast(settings, PipelineCompilationSettings).model_dump()}. Compiling ..."
    )

    compiled_word_embedding_pipeline_settings = cast(
        settings, PipelineCompilationSettings
    ).model_dump(exclude={"word_pipeline_max_length", "document_pipeline_max_length"})

    compiled_word_embedding_pipeline_settings.update(
        {"max_length": settings.word_pipeline_max_length}
    )

    compiled_word_embedding_pipeline = CompiledPipeline.from_pipeline(
        pipeline=base_model_pipeline, **compiled_word_embedding_pipeline_settings
    )

    compiled_document_embedding_pipeline_settings = cast(
        settings, PipelineCompilationSettings
    ).model_dump(exclude={"word_pipeline_max_length", "document_pipeline_max_length"})

    compiled_document_embedding_pipeline_settings.update(
        {"max_length": settings.word_pipeline_max_length}
    )

    compiled_document_embedding_pipeline = CompiledPipeline.from_pipeline(
        pipeline=base_model_pipeline,
        **compiled_document_embedding_pipeline_settings,
    )

    # assemble compiled keybert model
    compiled_keybert = CompiledKeyBERT(
        document_pipeline=compiled_document_embedding_pipeline,
        compiled_word_pipeline=compiled_word_embedding_pipeline,
    )

    # export compiled keybert model for next workflow component: test
    compiled_keybert.save_pretrained(
        settings.model_directory(CompileWorkflowTasks.COMPILE)
    )

    logger.debug(
        f"Successfully exported compiled model to {settings.model_directory(CompileWorkflowTasks.COMPILE)}"
    )


if __name__ == "__main__":
    settings = get_settings()
    init_logging(cast(settings, OnclusiveLogSettings))
    main(settings)
