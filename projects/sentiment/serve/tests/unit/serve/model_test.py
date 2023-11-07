"""Model test."""

# Standard Library
from unittest.mock import patch

# Internal libraries
from onclusiveml.models.sentiment import CompiledSent

# Source
from src.serve.artifacts import ServedModelArtifacts


def test_served_model_init(served_model):
    """Test served model initialization."""
    assert isinstance(served_model.served_model_artifacts, ServedModelArtifacts)
    assert not served_model.ready


@patch.object(CompiledSent, "from_pretrained")
def test_served_model_load(mock_from_pretrained, served_model):
    """Test served model load."""
    assert not served_model.ready
    served_model.load()
    assert served_model.ready

    mock_from_pretrained.assert_called_with(
        served_model.served_model_artifacts.model_artifact_directory
    )
