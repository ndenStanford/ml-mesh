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
from onclusiveml.models.iptc import CompiledIPTC
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
    # re-load the base model pipeline
    text_classification_pipeline = pipeline(
        task="text-classification",
        model=settings.model_directory(CompileWorkflowTasks.DOWNLOAD),
    )

    logger.debug(
        f"Using the following iptc pipeline compilation settings: "
        f"{cast(settings, PipelineCompilationSettings).model_dump()}. Compiling ..."
    )

    compiled_iptc_pipeline = CompiledPipeline.from_pipeline(
        pipeline=text_classification_pipeline,
        **cast(settings, PipelineCompilationSettings).model_dump(),
    )

    compiled_iptc = CompiledIPTC(
        project=settings.project,
        compiled_iptc_pipeline=compiled_iptc_pipeline,
    )

    # export compiled iptc model for next workflow component: test
    compiled_iptc.save_pretrained(
        settings.model_directory(CompileWorkflowTasks.COMPILE)
    )

    logger.debug(
        f"Successfully exported compiled iptc model to {settings.model_directory(CompileWorkflowTasks.COMPILE)}"
    )


if __name__ == "__main__":
    settings = get_settings()
    init_logging(cast(settings, OnclusiveLogSettings))
    main(settings)
