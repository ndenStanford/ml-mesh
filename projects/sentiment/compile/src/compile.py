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
from onclusiveml.models.sentiment import CompiledSentiment
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
        api_token=(
            settings.api_token.get_secret_value()
            if settings.api_token is not None
            else None
        ),
        project=settings.project,
    )
    # get base model card
    model_card: Dict = model_version.download_config_from_model_version(
        "model/model_card"
    )
    logger.debug(f"Base model model_card: {model_card}")
    # re-load base model pipeline
    model_pipeline = pipeline(
        task=model_card["model_params"]["huggingface_pipeline_task"],
        model=settings.model_directory(CompileWorkflowTasks.DOWNLOAD),
    )

    # compile model pipeline

    logger.debug(
        f"Using the following iptc pipeline compilation settings: "
        f"{cast(settings, PipelineCompilationSettings).model_dump()}. Compiling ..."
    )

    compiled_sent_pipeline = CompiledPipeline.from_pipeline(
        pipeline=model_pipeline,
        **cast(settings, PipelineCompilationSettings).model_dump(),
    )

    compiled_sent = CompiledSentiment(compiled_sent_pipeline)
    # export compiled sent model for next workflow component: test
    compiled_sent.save_pretrained(
        settings.model_directory(CompileWorkflowTasks.COMPILE)
    )

    logger.info(
        f"Successfully exported compiled sent model to {settings.model_directory(CompileWorkflowTasks.COMPILE)}"
    )


if __name__ == "__main__":
    settings = get_settings()
    init_logging(cast(settings, OnclusiveLogSettings))
    main(settings)
