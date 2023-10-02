"""Compile, validate and upload model."""

# 3rd party libraries
import pytest

# Source
from src.compile_model import compile_model
from src.download_uncompiled_model import download_uncompiled_model
from src.settings import (  # type: ignore[attr-defined]
    CompiledNERTrackedModelCard,
    CompiledTrackedModelSpecs,
    CompilePipelineExecutionSettings,
    CompilePipelineIOSettings,
    NERPipelineCompilationSettings,
    UncompiledTrackedModelSpecs,
)
from src.upload_compiled_model import upload_compiled_model


def run_compile_pipeline() -> None:
    """Run the compile pipeline."""
    compile_pipeline_execution_settings = CompilePipelineExecutionSettings()
    compile_pipeline_io_settings = CompilePipelineIOSettings()
    # initialize common settings classes
    base_model_specs = UncompiledTrackedModelSpecs()
    # download uncompiled model if specified
    if compile_pipeline_execution_settings.download:
        download_uncompiled_model(
            io_settings=compile_pipeline_io_settings, base_model_specs=base_model_specs
        )
    # compile model if specified
    if compile_pipeline_execution_settings.compile:
        ner_pipeline_compilation_settings = NERPipelineCompilationSettings()

        compile_model(
            io_settings=compile_pipeline_io_settings,
            base_model_specs=base_model_specs,
            ner_pipeline_compilation_settings=ner_pipeline_compilation_settings,
        )
    # validate compiled model if specified
    if compile_pipeline_execution_settings.test:
        pytest.main(["-x", "src/test_compiled_model"])
    # upload compiled model if specified
    if compile_pipeline_execution_settings.upload:
        # base model specs require write mode in this step
        base_model_specs = UncompiledTrackedModelSpecs(mode="async")
        compiled_model_specs = CompiledTrackedModelSpecs()
        compiled_model_card = CompiledNERTrackedModelCard()

        upload_compiled_model(
            io_settings=compile_pipeline_io_settings,
            base_model_specs=base_model_specs,
            compiled_model_specs=compiled_model_specs,
            compiled_model_card=compiled_model_card,
        )


if __name__ == "__main__":
    run_compile_pipeline()
