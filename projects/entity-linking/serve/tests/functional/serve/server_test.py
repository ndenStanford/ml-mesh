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
                                "entity_text": "CEO",
                                "score": 0.24852901697158813,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q484876",
                                "wiki_score": 0.48496711254119873,
                            },
                            {
                                "entity_text": "Apple",
                                "score": 0.7043066024780273,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
                                "wiki_score": 0.9504453539848328,
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
                                "entity_text": "CEO",
                                "score": 0.46443355083465576,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q484876",
                                "wiki_score": 0.6950671076774597,
                            },
                            {
                                "entity_text": "Apple",
                                "score": 0.79751056432724,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
                                "wiki_score": 0.9626907706260681,
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
                                "entity_text": "Steve Jobs",
                                "score": 0.8623836040496826,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q19837",
                                "wiki_score": 0.9862053990364075,
                            },
                            {
                                "entity_text": "Apple",
                                "score": 0.6849206686019897,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
                                "wiki_score": 0.9424868822097778,
                            },
                            {
                                "entity_text": "Elon Musk",
                                "score": 0.8932482004165649,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q317521",
                                "wiki_score": 0.9890680909156799,
                            },
                            {
                                "entity_text": "Tesla",
                                "score": 0.6265523433685303,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q478214",
                                "wiki_score": 0.9453710317611694,
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
                        "mention_offsets": [[0], [26], [61], [85]],
                        "mention_lengths": [[10], [5], [9], [5]],
                        "entities": [[0], [0], [0], [0]],
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
                                "entity_text": "Steve Jobs",
                                "score": None,
                                "sentence_index": None,
                                "wiki_link": "https://www.wikidata.org/wiki/Q19837",
                                "wiki_score": 0.4764402770996094,
                            },
                            {
                                "entity_text": "Apple",
                                "score": None,
                                "sentence_index": None,
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
                                "wiki_score": 0.36141754150390625,
                            },
                            {
                                "entity_text": "Elon Musk",
                                "score": None,
                                "sentence_index": None,
                                "wiki_link": "https://www.wikidata.org/wiki/Q317521",
                                "wiki_score": 0.48770980834960936,
                            },
                            {
                                "entity_text": "Tesla",
                                "score": None,
                                "sentence_index": None,
                                "wiki_link": "https://www.wikidata.org/wiki/Q478214",
                                "wiki_score": 0.35195270538330076,
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
