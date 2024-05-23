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
    root_response = requests.get("http://serve:8000/sentiment/v2/")

    assert root_response.status_code == 200


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/sentiment/v2/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/sentiment/v2/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/sentiment/v2/bio")

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
                        "content": "London is a wonderful city. John is a terrible man.",
                        "entities": [
                            {
                                "entity_type": "LOC",
                                "entity_text": "London",
                                "score": "0.99966383",
                                "sentence_index": 0,
                                "start": 0,
                                "end": 6,
                            },
                            {
                                "entity_type": "PER",
                                "entity_text": "John",
                                "score": "0.9991505",
                                "sentence_index": 1,
                                "start": 0,
                                "end": 4,
                            },
                        ],
                    },
                    "parameters": {
                        "language": "en",
                    },
                }
            },
            {
                "version": 2,
                "data": {
                    "identifier": None,
                    "namespace": "sentiment",
                    "attributes": {
                        "label": "positive",
                        "negative_prob": 0.4854,
                        "positive_prob": 0.4794,
                        "entities": [
                            {
                                "entity_type": "LOC",
                                "entity_text": "London",
                                "score": 0.99966383,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 6,
                                "sentiment": "positive",
                            },
                            {
                                "entity_type": "PER",
                                "entity_text": "John",
                                "score": 0.9991505,
                                "sentence_index": 1,
                                "start": 0,
                                "end": 4,
                                "sentiment": "negative",
                            },
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
        "http://serve:8000/sentiment/v2/predict",
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
                "version": 2,
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
        "http://serve:8000/sentiment/v2/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        # Test case for an unsupported language (invalid language code)
        (
            {
                "data": {
                    "namespace": "sentiment",
                    "attributes": {
                        "content": "Esta es una prueba con un idioma no soportado.",
                        "entities": [],
                    },
                    "parameters": {
                        "language": "xyz",
                    },
                }
            },
            {
                "status": 422,
                "detail": "The language reference 'xyz' could not be mapped",
            },
        ),
        # Test case for a correct but unsupported language code
        (
            {
                "data": {
                    "namespace": "sentiment",
                    "attributes": {
                        "content": "Dit is 'n toets in 'n nie-ondersteunde taal.",
                        "entities": [],
                    },
                    "parameters": {
                        "language": "af",
                    },
                }
            },
            {
                "status": 422,
                "detail": "The language 'LanguageIso.AF' that was looked up from 'af'",
            },
        ),
        # Test case for Chinese
        (
            {
                "data": {
                    "namespace": "sentiment",
                    "attributes": {
                        "content": "北京是中国的首都。",
                        "entities": [
                            {
                                "entity_type": "LOC",
                                "entity_text": "北京",
                                "score": "0.9999",
                                "sentence_index": 0,
                                "start": 0,
                                "end": 2,
                            },
                        ],
                    },
                    "parameters": {
                        "language": "zh",
                    },
                }
            },
            {
                "version": 2,
                "data": {
                    "identifier": None,
                    "attributes": {
                        "entities": [
                            {
                                "end": 2,
                                "entity_text": "北京",
                                "entity_type": "LOC",
                                "score": 0.9999,
                                "sentence_index": 0,
                                "sentiment": "positive",
                                "start": 0,
                            }
                        ],
                        "label": "positive",
                        "negative_prob": 0.1478,
                        "positive_prob": 0.3239,
                    },
                    "namespace": "sentiment",
                },
            },
        ),
    ],
)
def test_new_language_cases(payload, expected_response):
    """Tests the sentiment prediction endpoint for new language scenarios."""
    response = requests.post(
        "http://serve:8000/sentiment/v2/predict",
        json=payload,
    )

    if response.status_code != 200:
        assert response.status_code == expected_response.get("status", 500)
        assert response.json()["detail"].startswith(expected_response["detail"])
    else:
        assert response.status_code == 200
        assert response.json() == expected_response
