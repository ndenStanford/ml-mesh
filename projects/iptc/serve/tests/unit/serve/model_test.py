"""Model test."""

# Standard Library
from unittest.mock import patch

# Internal libraries
from onclusiveml.models.iptc import CompiledIPTC

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.settings import get_settings


def test_served_model_init(served_model):
    """Test served model initialization."""
    assert isinstance(served_model.served_model_artifacts, ServedModelArtifacts)
    assert not served_model.ready


@patch.object(CompiledIPTC, "from_pretrained")
def test_served_model_load(mock_from_pretrained, served_model):
    """Test served model load."""
    assert not served_model.ready
    served_model.load()
    assert served_model.ready

    mock_from_pretrained.assert_called_with(
        get_settings().project,
        served_model.served_model_artifacts.model_artifact_directory,
    )
