"""Model test."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.models.sentiment import CompiledSentiment

# Source
from src.serve.artifacts import ServedModelArtifacts


def test_served_model_init(served_model):
    """Test served model initialization."""
    assert isinstance(served_model.served_model_artifacts, ServedModelArtifacts)
    assert not served_model.ready


@patch.object(CompiledSentiment, "from_pretrained")
def test_served_model_load(mock_from_pretrained, served_model):
    """Test served model load."""
    assert not served_model.ready
    served_model.load()
    assert served_model.ready

    mock_from_pretrained.assert_called_with(
        served_model.served_model_artifacts.model_artifact_directory
    )


@pytest.mark.parametrize(
    "content, expected_result",
    [
        ("Short", False),
        ("This sentence is long enough.", True),
        ("   Spaces   around   ", False),
        ("!@#$%^&*()_+", False),
        ("Valid with some !@#$% punctuation.", True),
        ("", False),
        (" ", False),
        ("This is a sentence with numbers 123 and symbols !@#.", True),
        ("Thísíßåñexåmple∑ithünicode", True),
    ],
)
def test_validate_content(served_model, content, expected_result):
    """Test validate content method."""
    assert served_model.validate_content(content) == expected_result
