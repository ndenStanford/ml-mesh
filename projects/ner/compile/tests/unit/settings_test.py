"""Settings tests."""

# Source
from src.settings import (
    CompiledNERTrackedModelCard,
    CompiledTrackedModelSettings,
    IOSettings,
)


def test_io_settings():
    """Test io settings."""
    IOSettings()


def test_compiled_tracked_model_specs():
    """Test compiled tracked model specs."""
    CompiledTrackedModelSettings()


def test_compiled_ner_tracked_model_card():
    """Test compiled NER tracked model card."""
    CompiledNERTrackedModelCard()
