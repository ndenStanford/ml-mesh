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
    assert liveness_response.model_dump_json() == LivenessProbeResponse().model_dump()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/ner/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.model_dump_json() == ReadinessProbeResponse().model_dump()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/ner/v1/bio")

    assert readiness_response.status_code == 200
    assert (
        readiness_response.model_dump_json()["data"]["attributes"].get("model_card")
        is not None
    )


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        # Test case for English (no entity)
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
        # Test case for Korean (with entities)
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
                                "score": 0.9980051755905152,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 5,
                            },
                            {
                                "entity_text": "제공마우이 신속대응",
                                "entity_type": "ORG",
                                "score": 0.7580916749106513,
                                "sentence_index": 0,
                                "start": 17,
                                "end": 27,
                            },
                        ]
                    },
                },
            },
        ),
        # Test case for English (with entities)
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
                                "score": 0.9364089369773865,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 6,
                            },
                            {
                                "entity_text": "AI",
                                "entity_type": "MISC",
                                "score": 0.9874637126922607,
                                "sentence_index": 0,
                                "start": 16,
                                "end": 18,
                            },
                            {
                                "entity_text": "Anthropic",
                                "entity_type": "MISC",
                                "score": 0.8394989768664042,
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
    assert response.model_dump_json() == expected_response


@pytest.mark.parametrize(
    "payload,expected_error_detail",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": "Irrelevant content because of invalid message value (nonsense)."
                    },
                    "parameters": {"language": "invalid_language"},
                }
            },
            "The language reference 'invalid_language' could not be mapped, or the language could not be inferred from the content.",  # noqa: E501
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": "Second example of irrelevant content because of invalid message value (empty string)."  # noqa: E501
                    },
                    "parameters": {"language": ""},
                }
            },
            "The language reference '' could not be mapped, or the language could not be inferred from the content.",  # noqa: E501
        ),
    ],
)
def test_model_server_prediction_invalid_language(payload, expected_error_detail):
    """Tests the language validation of the predict endpoint of a running ModelServer instance."""
    response = requests.post(
        "http://serve:8000/ner/v1/predict",
        json=payload,
    )

    assert response.status_code == 204
    assert response.text == ""
