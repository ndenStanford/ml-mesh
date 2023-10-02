"""Settings tests."""

# Source
from src.settings import (
    CompiledNERTrackedModelCard,
    CompiledTrackedModelSpecs,
    CompilePipelineExecutionSettings,
    CompilePipelineIOSettings,
)


def test_compile_pipeline_io_settings():
    """Test compile pipeline io settings."""
    CompilePipelineIOSettings()


def test_compile_pipeline_execution_settings():
    """Test compile pipeline execution setting."""
    CompilePipelineExecutionSettings()


def test_compiled_tracked_model_specs():
    """Test compiled tracked model specs."""
    CompiledTrackedModelSpecs()


def test_compiled_ner_tracked_model_card():
    """Test compiled NER tracked model card."""
    CompiledNERTrackedModelCard()
