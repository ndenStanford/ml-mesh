"""Settings test."""

# Source
from src.settings import (
    TrackedSummarizationModelCard,
    TrackedSummarizationModelSpecs,
)


def test_tracked_sum_model_specs():
    """Test tracked summarization model settings."""
    TrackedSummarizationModelSpecs()


def test_tracked_sum_model_card():
    """Test tracked summarization model card."""
    TrackedSummarizationModelCard()
