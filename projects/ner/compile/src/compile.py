"""Compile model."""

# Standard Library
import os
from typing import Dict

# ML libs
from transformers import pipeline

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.base.pydantic import cast
from onclusiveml.core.logging import OnclusiveLogSettings, get_default_logger
from onclusiveml.models.ner import CompiledNER
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    NERPipelineCompilationSettings,
    TrackedModelSettings,
    get_settings,
)


def compile(settings: OnclusiveBaseSettings) -> None:
    """Compile model."""
    # cast settings
    logging_settings = cast(settings, OnclusiveLogSettings)
    tracked_model_settings = cast(settings, TrackedModelSettings)
    ner_pipeline_compilation_settings = cast(settings, NERPipelineCompilationSettings)

    logger = get_default_logger(
        name=__name__,
        fmt_level=logging_settings.fmt_level,
        level=logging_settings.level,
        json_format=logging_settings.json_format,
    )
    # model directories
    source_model_directory: str = os.path.join(
        "./outputs", "download", "model_artifacts"
    )
    target_model_directory: str = os.path.join(
        "./outputs", "compile", "model_artifacts"
    )

    base_model_version = TrackedModelVersion(**tracked_model_settings.model_dump())
    # get base model card
    base_model_card: Dict = base_model_version.download_config_from_model_version(
        "model/model_card"
    )

    logger.debug(f"Base model model_card: {base_model_card}")
    # re-load base model pipeline
    ner_model_pipeline_base = pipeline(
        task=base_model_card["ner_model_params_base"]["huggingface_pipeline_task"],
        model=os.path.join(source_model_directory, "base_ner"),
    )
    ner_model_pipeline_korean_and_japanese = pipeline(
        task=base_model_card["ner_model_params_kj"]["huggingface_pipeline_task_kj"],
        model=os.path.join(source_model_directory, "korean_japanese_ner"),
    )

    logger.debug(
        f"Using the following ner pipeline compilation settings: "
        f"{ner_pipeline_compilation_settings.model_dump()}. Compiling ..."
    )

    compiled_ner_pipeline_base = CompiledPipeline.from_pipeline(
        pipeline=ner_model_pipeline_base,
        **ner_pipeline_compilation_settings.model_dump(exclude={"pipeline_name"}),
    )

    compiled_ner_pipeline_korean_and_japanese = CompiledPipeline.from_pipeline(
        pipeline=ner_model_pipeline_korean_and_japanese,
        **ner_pipeline_compilation_settings.model_dump(exclude={"pipeline_name"}),
    )

    compiled_ner = CompiledNER(
        compiled_ner_pipeline_base=compiled_ner_pipeline_base,
        compiled_ner_pipeline_korean_and_japanese=compiled_ner_pipeline_korean_and_japanese,
    )
    # export compiled ner model for next workflow component: test
    compiled_ner.save_pretrained(target_model_directory)

    logger.info(f"Successfully exported compiled ner model to {target_model_directory}")


if __name__ == "__main__":
    compile(get_settings())
