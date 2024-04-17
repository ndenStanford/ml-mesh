"""Settings test."""

# Source
from src.settings import (
    TrackedDocumentContentScoringModelCard,
    TrackedDocumentContentScoringSpecs,
)


def test_tracked_content_scoring_model_specs():
    """Tracked content-scoring model settings test."""
    TrackedDocumentContentScoringSpecs()


def test_tracked_content_scoring_base_model_card():
    """Tracked content-scoring model card test."""
    TrackedDocumentContentScoringModelCard()
