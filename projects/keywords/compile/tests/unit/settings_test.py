"""Settings test."""

# Source
from src.settings import (
    CompiledKeywordsTrackedModelCard,
    CompiledTrackedModelSpecs,
    CompilePipelineExecutionSettings,
    CompilePipelineIOSettings,
)


def test_io_settings():
    """Tests pipeline IO settings."""
    CompilePipelineIOSettings()


def test_compile_pipeline_execution_settings():
    """Tests pipeline execution settings."""
    CompilePipelineExecutionSettings()


def test_compiled_tracked_model_specs():
    """Tests Compiled tracked model specs."""
    CompiledTrackedModelSpecs()


def test_compiled_keywords_tracked_model_card():
    """Tests compiled keywords model card."""
    CompiledKeywordsTrackedModelCard()
