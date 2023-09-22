"""Compile, validate and upload model."""

# 3rd party libraries
import pytest

# Source
from src.compile_model import compile_model
from src.download_uncompiled_model import download_uncompiled_model
from src.settings import (  # type: ignore[attr-defined]
    CompiledKeywordsTrackedModelCard,
    CompiledTrackedModelSpecs,
    CompilePipelineSettings,
    DocumentPipelineCompilationSettings,
    IOSettings,
    UncompiledTrackedModelSpecs,
    WordPipelineCompilationSettings,
)
from src.upload_compiled_model import upload_compiled_model


def run_compile_pipeline() -> None:
    """Run the compile pipeline."""
    compile_pipeline_settings = CompilePipelineSettings()
    # initialize common settings classes
    io_settings = IOSettings()
    base_model_specs = UncompiledTrackedModelSpecs()
    # download uncompiled model if specified
    if compile_pipeline_settings.download_uncompiled_model:
        download_uncompiled_model(
            io_settings=io_settings, base_model_specs=base_model_specs
        )
    # compile model if specified
    if compile_pipeline_settings.compile_model:
        word_pipeline_compilation_settings = WordPipelineCompilationSettings()
        document_pipeline_compilation_settings = DocumentPipelineCompilationSettings()

        compile_model(
            io_settings=io_settings,
            base_model_specs=base_model_specs,
            word_pipeline_compilation_settings=word_pipeline_compilation_settings,
            document_pipeline_compilation_settings=document_pipeline_compilation_settings,
        )
    # validate compiled model if specified
    if compile_pipeline_settings.validate_compiled_model:
        pytest.main(["-x", "src/test_compiled_model"])
    # upload compiled model if specified
    if compile_pipeline_settings.upload_compiled_model:
        # base model specs require write mode in this step
        base_model_specs = UncompiledTrackedModelSpecs(mode="async")
        compiled_model_specs = CompiledTrackedModelSpecs()
        compiled_model_card = CompiledKeywordsTrackedModelCard()

        upload_compiled_model(
            io_settings=io_settings,
            base_model_specs=base_model_specs,
            compiled_model_specs=compiled_model_specs,
            compiled_model_card=compiled_model_card,
        )


if __name__ == "__main__":
    run_compile_pipeline()
