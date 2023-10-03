"""Settings test."""

# Source
from src.settings import TrackedSumModelCard, TrackedSumModelSpecs


def test_tracked_sum_model_specs():
    """Test tracked summarization model settings."""
    TrackedSumModelSpecs()


def test_tracked_sum_model_card():
    """Test tracked summarization model card."""
    TrackedSumModelCard()