"""Server functional tests."""

# 3rd party libraries
import pytest
import requests

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


def test_model_server_root():
    """Tests the root endpoint of a ModelServer (not running) instance."""
    root_response = requests.get("http://serve:8000/sentiment/v1/")

    assert root_response.status_code == 200


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/sentiment/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/sentiment/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/sentiment/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_card") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "namespace": "sentiment",
                    "attributes": {
                        "content": "London is a wonderful city.",
                        "entities": [
                            {
                                "entity_type": "LOC",
                                "entity_text": "London",
                                "score": "0.99966383",
                                "sentence_index": 0,
                                "start": 0,
                                "end": 6,
                            },
                        ],
                    },
                    "parameters": {
                        "language": "en",
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "sentiment",
                    "attributes": {
                        "label": "positive",
                        "negative_prob": 0.0174,
                        "positive_prob": 0.9418,
                        "entities": [
                            {
                                "entity_type": "LOC",
                                "entity_text": "London",
                                "score": 0.99966383,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 6,
                                "sentiment": "neutral",
                            }
                        ],
                    },
                },
            },
        )
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/sentiment/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "namespace": "sentiment",
                    "attributes": {"content": "AI is a fantastic tool."},
                    "parameters": {"language": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "sentiment",
                    "attributes": {
                        "label": "positive",
                        "negative_prob": 0.0256,
                        "positive_prob": 0.9139,
                        "entities": None,
                    },
                },
            },
        )
    ],
)
def test_model_server_prediction_no_entities(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/sentiment/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response
