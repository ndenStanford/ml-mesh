"""Settings test."""

# Source
from src.settings import (
    CompiledSentTrackedModelCard,
    CompiledTrackedModelSpecs,
    IOSettings,
)


def test_io_settings():
    """Test IO settings."""
    IOSettings()


def test_compiled_tracked_model_specs():
    """Test compiled tracked model settings."""
    CompiledTrackedModelSpecs()


def test_compiled_ner_tracked_model_card():
    """Test compiled NER tracked model card."""
    CompiledSentTrackedModelCard()
