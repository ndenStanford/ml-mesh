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
                    "attributes": {"content": "Jobs was CEO of Apple"},  # noqa
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
                                "entity_type": None,
                                "entity_text": "CEO",
                                "score": 0.24852901697158813,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q484876",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Apple",
                                "score": 0.7043066024780273,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
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
                    "namespace": "entity-linking",
                    "attributes": {"content": "Jobs war der CEO von Apple"},  # noqa
                    "parameters": {"lang": "de"},
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
                                "entity_type": None,
                                "entity_text": "CEO",
                                "score": 0.46443355083465576,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q484876",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Apple",
                                "score": 0.79751056432724,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
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
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "Steve Jobs was CEO of Apple. Hello, nothing to see here. Elon Musk is the CEO of Tesla."  # noqa
                    },  # noqa
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
                                "entity_type": None,
                                "entity_text": "Steve Jobs",
                                "score": 0.8623836040496826,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q19837",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Apple",
                                "score": 0.6849206686019897,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Elon Musk",
                                "score": 0.8932482004165649,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q317521",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Tesla",
                                "score": 0.6265523433685303,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q478214",
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
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "Steve Jobs was the CEO of Apple. Hello, nothing to see here. Elon Musk is the CEO of Tesla. That is it.",  # noqa
                        "entities": [
                            {
                                "entity_type": "PER",
                                "entity_text": "Steve Jobs",
                                "score": 0.9995638926823934,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q19837",
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Apple",
                                "score": 0.999211311340332,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
                            },
                            {
                                "entity_type": "PER",
                                "entity_text": "Elon Musk",
                                "score": 0.9523038864135742,
                                "sentence_index": [2],
                                "wiki_link": "https://www.wikidata.org/wiki/Q317521",
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Tesla",
                                "score": 0.9936597347259521,
                                "sentence_index": [2],
                                "wiki_link": "https://www.wikidata.org/wiki/Q478214",
                            },
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
                                "entity_type": "PER",
                                "entity_text": "Steve Jobs",
                                "score": 0.9995638926823934,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q19837",
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Apple",
                                "score": 0.999211311340332,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
                            },
                            {
                                "entity_type": "PER",
                                "entity_text": "Elon Musk",
                                "score": 0.9523038864135742,
                                "sentence_index": [2],
                                "wiki_link": "https://www.wikidata.org/wiki/Q317521",
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Tesla",
                                "score": 0.9936597347259521,
                                "sentence_index": [2],
                                "wiki_link": "https://www.wikidata.org/wiki/Q478214",
                            },
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

    assert response.status_code == 422
    assert response.json()["detail"].startswith(expected_error_detail)
