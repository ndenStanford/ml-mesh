"""Settings test."""

# Source
from src.settings import (
    TrackedDocumentEvaluatorModelCard,
    TrackedDocumentEvaluatorSpecs,
)


def test_tracked_evaluator_model_specs():
    """Tracked Evaluator model settings test."""
    TrackedDocumentEvaluatorSpecs()


def test_tracked_evaluator_base_model_card():
    """Tracked Evaluator model card test."""
    TrackedDocumentEvaluatorModelCard()
