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
from onclusiveml.models.ner import CompiledNER
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    IOSettings,
    NERPipelineCompilationSettings,
    UncompiledTrackedModelSpecs,
)


def main() -> None:
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
    ner_model_pipeline_base = pipeline(
        task=base_model_card["ner_model_params_base"]["huggingface_pipeline_task"],
        model=io_settings.download.model_directory_base,
    )
    ner_model_pipeline_kj = pipeline(
        task=base_model_card["ner_model_params_kj"]["huggingface_pipeline_task_kj"],
        model=io_settings.download.model_directory_kj,
    )
    # compile base model pipeline for NER
    ner_pipeline_compilation_settings = NERPipelineCompilationSettings()

    logger.debug(
        f"Using the following ner pipeline compilation settings: "
        f"{ner_pipeline_compilation_settings.dict()}. Compiling ..."
    )

    compiled_ner_pipeline_base = CompiledPipeline.from_pipeline(
        pipeline=ner_model_pipeline_base,
        **ner_pipeline_compilation_settings.dict(exclude={"pipeline_name"}),
    )

    compiled_ner_pipeline_kj = CompiledPipeline.from_pipeline(
        pipeline=ner_model_pipeline_kj,
        **ner_pipeline_compilation_settings.dict(exclude={"pipeline_name"}),
    )

    compiled_ner = CompiledNER(
        compiled_ner_pipeline_base=compiled_ner_pipeline_base,
        compiled_ner_pipeline_kj=compiled_ner_pipeline_kj,
    )
    # export compiled ner model for next workflow component: test
    compiled_ner.save_pretrained(io_settings.compile.model_directory)

    logger.debug(
        f"Successfully exported compiled ner models to {io_settings.compile.model_directory}"
    )


if __name__ == "__main__":
    main()
