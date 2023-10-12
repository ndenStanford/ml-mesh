"""Settings test."""

# Source
from src.settings import (
    CompiledKeywordsTrackedModelCard,
    CompiledTrackedModelSpecs,
    IOSettings,
)


def test_io_settings():
    """Tests IO settings."""
    IOSettings()


def test_compiled_tracked_model_specs():
    """Tests Compiled tracked model specs."""
    CompiledTrackedModelSpecs()


def test_compiled_keywords_tracked_model_card():
    """Tests compiled keywords model card."""
    CompiledKeywordsTrackedModelCard()
