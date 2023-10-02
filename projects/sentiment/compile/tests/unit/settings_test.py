"""Settings test."""

# Source
from src.settings import (
    CompiledSentTrackedModelCard,
    CompiledTrackedModelSpecs,
    CompilePipelineExecutionSettings,
    CompilePipelineIOSettings,
)


def test_compile_pipeline_io_settings():
    """Test compile pipeline IO settings fixture."""
    CompilePipelineIOSettings()


def test_compile_pipeline_execution_settings():
    """Test compile pipeline execution settings."""
    CompilePipelineExecutionSettings()


def test_compiled_tracked_model_specs():
    """Test compiled tracked model settings."""
    CompiledTrackedModelSpecs()


def test_compiled_ner_tracked_model_card():
    """Test compiled NER tracked model card."""
    CompiledSentTrackedModelCard()
