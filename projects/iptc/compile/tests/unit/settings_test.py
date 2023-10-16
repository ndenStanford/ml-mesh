"""Settings test."""

# Source
from src.settings import (
    CompiledIPTCTrackedModelCard,
    CompiledTrackedModelSpecs,
    IOSettings,
)


def test_io_settings():
    """IO settings fixture."""
    IOSettings()


def test_compiled_tracked_model_specs():
    """Compiled tracked model settings."""
    CompiledTrackedModelSpecs()


def test_compiled_iptc_tracked_model_card():
    """Compiled IPTC tracked model card."""
    CompiledIPTCTrackedModelCard()
