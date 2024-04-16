"""Model test."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.models.content_scoring import CompiledContentScoring

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.model import ServedContentScoringModel
from src.serve.schemas import PredictRequestSchema, PredictResponseSchema


def test_served_model_init(served_model):
    """Test served model initialization."""
    assert isinstance(served_model.served_model_artifacts, ServedModelArtifacts)
    assert not served_model.ready


@patch.object(CompiledContentScoring, "from_pretrained")
def test_served_model_load(mock_from_pretrained, served_model):
    """Test served model load."""
    assert not served_model.ready
    served_model.load()
    assert served_model.ready


@pytest.mark.parametrize(
    "payload, predict_return, expected_response",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "content-scoring",
                    "attributes": {
                        "data": {
                            "pagerank": [3.299923, 9.1, 9.4],
                            "reach": [90, 2821568, 3614746],
                            "score": [628226.6, 4213572.0, 1601918.4],
                            "lang": [2.0, 2.0, 0.0],
                            "media_type": [3.0, 3.0, 3.0],
                            "label": [1.0, 1.0, 2.0],
                            "publication": [72.0, 69.0, 43.0],
                            "country": [1.0, 1.0, 2.0],
                            "is_copyrighted": [0.0, 0.0, 0.0],
                            "type_of_summary": [0.0, 0.0, 0.0],
                        }
                    },
                    "parameters": {},
                }
            },
            ["rejected", "rejected", "accepted"],
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "content-scoring",
                    "attributes": {
                        "boolean_messages": ["rejected", "rejected", "accepted"]
                    },
                },
            },
        ),
    ],
)
@patch.object(ServedContentScoringModel, "model")
@patch.object(CompiledContentScoring, "from_pretrained")
def test_served_model_predict(
    from_pretrained_mock,
    model_call_mock,
    served_model,
    payload,
    predict_return,
    expected_response,
):
    """Test served model predict method."""
    model_call_mock.return_value.inference.return_value = predict_return

    served_model.load()
    response = served_model.predict(PredictRequestSchema(**payload))

    assert isinstance(response, PredictResponseSchema)

    response.version == expected_response["version"]
    response.data.identifier == expected_response["data"]["identifier"]
    response.data.namespace == expected_response["data"]["namespace"]
    response.data.attributes == expected_response["data"]["attributes"]
