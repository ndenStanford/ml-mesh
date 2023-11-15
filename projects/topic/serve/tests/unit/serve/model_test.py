"""Model test."""

# Standard Library
from unittest.mock import patch

# Internal libraries
from onclusiveml.models.topic import TrainedTopic

# Source
from src.serve.artifacts import ServedModelArtifacts


def test_served_model_init(served_model):
    """Test served model initialization."""
    assert isinstance(served_model.served_model_artifacts, ServedModelArtifacts)
    assert not served_model.ready


@patch.object(TrainedTopic, "load_trained")
def test_served_model_load(mock_load_trained, served_model):
    """Test served model load."""
    assert not served_model.ready
    served_model.load()
    assert served_model.ready

    mock_load_trained.assert_called_with(
        served_model.served_model_artifacts.model_artifact_directory
    )
