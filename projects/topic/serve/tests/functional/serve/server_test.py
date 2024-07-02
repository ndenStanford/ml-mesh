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
    root_response = requests.get("http://serve:8000/topic/v1/")

    assert root_response.status_code == 200


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/topic/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().model_dump()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/topic/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().model_dump()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/topic/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_card") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "namespace": "topic",
                    "attributes": {
                        "content": "London is a wonderful city. John is a terrible man.",
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
                    "namespace": "topic",
                    "attributes": {
                        "topic_id": "861",
                        "topic_representation": [
                            "conventional",
                            "wars",
                            "conflicts",
                            "humanitarian",
                            "informal",
                            "afghanistan",
                            "ocean",
                            "migration",
                            "warfare",
                            "indian",
                        ],
                    },
                },
            },
        ),
        (
            {
                "data": {
                    "namespace": "topic",
                    "attributes": {
                        "content": "London is a wonderful city. John is a terrible man.",
                    },
                    "parameters": {
                        "language": "xyz",
                    },
                }
            },
            {
                "status": 204,
                "detail": "The language reference 'xyz' could not be mapped",
            },
        ),
        (
            {
                "data": {
                    "namespace": "topic",
                    "attributes": {
                        "content": "Dit is 'n toets in 'n nie-ondersteunde taal.",
                    },
                    "parameters": {
                        "language": "af",
                    },
                }
            },
            {
                "status": 204,
                "detail": "The language 'LanguageIso.AF' that was looked up from 'af'",
            },
        ),
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests predict endpoint of the topic ModelServer."""
    response = requests.post(
        "http://serve:8000/topic/v1/predict",
        json=payload,
    )
    if response.status_code != 200:
        assert response.status_code == expected_response.get("status", 500)
        assert response.text == ""
    else:
        assert response.status_code == 200
        # TODO: assert score close to expected
        assert response.json() == expected_response
