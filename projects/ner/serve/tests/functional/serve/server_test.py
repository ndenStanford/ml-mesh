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
    root_response = requests.get("http://serve:8000/ner/v1/")

    assert root_response.status_code == 200


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/ner/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/ner/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/ner/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_card") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": "House prices were unchanged last month, defying predictions of another drop, but they are unlikely to have troughed just yet."  # noqa
                    },
                    "parameters": {"language": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {"entities": []},
                },
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": "에어비앤비, 하와이 임시 거처 제공마우이 신속대응팀 등 비영리 단체와 지속 협력"
                    },
                    "parameters": {"language": "ko"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            {
                                "entity_text": "에어비앤비",
                                "entity_type": "ORG",
                                "score": 0.9979469299316406,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 5,
                            },
                            {
                                "entity_text": "제공마우이 신속대응",
                                "entity_type": "ORG",
                                "score": 0.7619035475783877,
                                "sentence_index": 0,
                                "start": 17,
                                "end": 27,
                            },
                        ]
                    },
                },
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": "Amazon steps up AI race with up to 4 billion deal to invest in Anthropic."  # noqa
                    },
                    "parameters": {"language": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            {
                                "entity_text": "Amazon",
                                "entity_type": "LOC",
                                "score": 0.9350188970565796,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 6,
                            },
                            {
                                "entity_text": "AI",
                                "entity_type": "MISC",
                                "score": 0.9877899885177612,
                                "sentence_index": 0,
                                "start": 16,
                                "end": 18,
                            },
                            {
                                "entity_text": "Anthropic",
                                "entity_type": "MISC",
                                "score": 0.8427480657895406,
                                "sentence_index": 0,
                                "start": 63,
                                "end": 72,
                            },
                        ]
                    },
                },
            },
        ),
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/ner/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response
