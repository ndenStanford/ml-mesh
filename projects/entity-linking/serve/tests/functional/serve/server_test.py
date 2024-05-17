"""Server functional tests."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


def test_model_server_root(test_client):
    """Tests the root endpoint of a running ModelServer instance."""
    root_response = test_client.get("/entity-linking/v1/")

    assert root_response.status_code == 200


def test_model_server_liveness(test_client):
    """Tests the liveness endpoint of a running ModelServer instance."""
    liveness_response = test_client.get("/entity-linking/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness(test_client):
    """Tests the readiness endpoint of a running ModelServer instance."""
    readiness_response = test_client.get("/entity-linking/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "House prices were unchanged last month, defying predictions of another drop, but they are unlikely to have troughed just yet."  # noqa
                    },
                    "parameters": {"lang": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {"entities": []},
                },
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "Tottenham Hotspur Football Club has drawn up plans for student flats on the site of a former printworks near its stadium."  # noqa
                    },
                    "parameters": {"lang": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "Tottenham Hotspur Football Club",
                                "score": 0.9259419441223145,
                                "sentence_index": 0,
                                "wiki_link": "https://www.wikidata.org/wiki/Q18741",
                            }
                        ]
                    },
                },
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "Tottenham Hotspur Football Club has drawn up plans for student flats on the site of a former printworks near its stadium.",  # noqa
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "text": "Tottenham Hotspur Football Club",
                                "salience_score": 0.9259419441223145,
                                "sentence_indexes": [0],
                            }
                        ],
                    },
                    "parameters": {"lang": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "Tottenham Hotspur Football Club",
                                "score": 0.9259419441223145,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q18741",
                            }
                        ]
                    },
                },
            },
        ),
    ],
)
def test_model_server_prediction(test_client, payload, expected_response):
    """Tests the predict endpoint of a running ModelServer instance."""
    response = test_client.post(
        "/entity-linking/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "payload,expected_error_detail",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "Irrelevant content because of invalid message value (nonsense)."
                    },
                    "parameters": {"lang": "invalid_language"},
                }
            },
            "The language reference 'invalid_language' could not be mapped, or the language could not be inferred from the content.",  # noqa: E501
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "Second example of irrelevant content because of invalid message value (empty string)."  # noqa: E501
                    },
                    "parameters": {"lang": ""},
                }
            },
            "The language reference '' could not be mapped, or the language could not be inferred from the content.",  # noqa: E501
        ),
    ],
)
def test_model_server_prediction_invalid_language(
    test_client, payload, expected_error_detail
):
    """Tests the language validation of the predict endpoint of a running ModelServer instance."""
    response = test_client.post(
        "/entity-linking/v1/predict",
        json=payload,
    )

    assert response.status_code == 400
    assert response.json()["detail"].startswith(expected_error_detail)
