"""Settings test."""

# Source
from src.settings import (  # type: ignore[attr-defined]
    TopicModelParams,
    TrackedTopicBaseModelCard,
    TrackedTopicModelSpecs,
)


def test_tracked_topic_model_specs():
    """Test tracked topic model specs."""
    TrackedTopicModelSpecs()


def test_tracked_topic_base_model_card():
    """Test tracked topic base model card."""
    TrackedTopicBaseModelCard()


def test_topic_model_params():
    """Test tracked topic base model card."""
    TopicModelParams()