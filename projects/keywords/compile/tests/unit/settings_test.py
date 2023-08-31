"""Settings test."""

# Source
from src.settings import (
    CompiledKeywordsTrackedModelCard,
    CompiledTrackedModelSpecs,
    IOSettings,
)


def test_io_settings():
    """IO settings fixture."""
    IOSettings()


def test_compiled_tracked_model_specs():
    """Compiled tracked model specs fixture."""
    CompiledTrackedModelSpecs()


def test_compiled_keywords_tracked_model_card():
    """Compiled keywords model card fixture."""
    CompiledKeywordsTrackedModelCard()
