"""Settings test."""

# Source
from src.settings import (
    TrackedEntityLinkingBaseModelCard,
    TrackedEntityLinkingModelSpecs,
)


def test_tracked_entity_linking_model_specs():
    """Test tracked entity linking model settings."""
    TrackedEntityLinkingModelSpecs()


def test_tracked_entity_linking_base_model_card():
    """Test tracked entity linking model card."""
    TrackedEntityLinkingBaseModelCard()
