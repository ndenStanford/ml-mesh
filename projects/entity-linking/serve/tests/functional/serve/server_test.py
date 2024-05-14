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
                                "entity_type": "UNK",
                                "text": "CEO",
                                "salience_score": 0.24852901697158813,
                                "sentence_indexes": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q484876",
                                "wiki_score": 0.48496711254119873
                            },
                            {
                                "entity_type": "UNK",
                                "text": "Apple",
                                "salience_score": 0.7043066024780273,
                                "sentence_indexes": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
                                "wiki_score": 0.9504453539848328
                            }
                        ]
                    }
                }
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
                                "entity_type": "UNK",
                                "text": "CEO",
                                "salience_score": 0.46443355083465576,
                                "sentence_indexes": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q484876",
                                "wiki_score": 0.6950671076774597
                            },
                            {
                                "entity_type": "UNK",
                                "text": "Apple",
                                "salience_score": 0.79751056432724,
                                "sentence_indexes": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
                                "wiki_score": 0.9626907706260681
                            }
                        ]
                    }
                }
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {"content": "Steve Jobs was CEO of Apple. Hello, nothing to see here. Elon Musk is the CEO of Tesla."},  # noqa
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
                                "entity_type": "UNK",
                                "text": "Steve Jobs",
                                "salience_score": 0.438759982585907,
                                "sentence_indexes": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q19837",
                                "wiki_score": 0.931149959564209
                            },
                            {
                                "entity_type": "UNK",
                                "text": "CEO",
                                "salience_score": 0.2891087830066681,
                                "sentence_indexes": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q484876",
                                "wiki_score": 0.5837497115135193
                            },
                            {
                                "entity_type": "UNK",
                                "text": "Apple",
                                "salience_score": 0.7522366046905518,
                                "sentence_indexes": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q312",
                                "wiki_score": 0.9569951295852661
                            },
                            {
                                "entity_type": "UNK",
                                "text": "Elon Musk",
                                "salience_score": 0.3659305274486542,
                                "sentence_indexes": [2],
                                "wiki_link": "https://www.wikidata.org/wiki/Q317521",
                                "wiki_score": 0.8962705135345459
                            },
                            {
                                "entity_type": "UNK",
                                "text": "CEO",
                                "salience_score": 0.28305891156196594,
                                "sentence_indexes": [2],
                                "wiki_link": "https://www.wikidata.org/wiki/Q484876",
                                "wiki_score": 0.578008234500885
                            },
                            {
                                "entity_type": "UNK",
                                "text": "Tesla",
                                "salience_score": 0.7223825454711914,
                                "sentence_indexes": [2],
                                "wiki_link": "https://www.wikidata.org/wiki/Q478214",
                                "wiki_score": 0.9659820199012756
                            }
                        ]
                    }
                }
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "Elon Musk is the CEO of Tesla. Hello, nothing to see here. Steve Jobs was CEO of Apple.",
                        "entities": [
                            {
                                "entity_type": "Pers",
                                "text": "Elon Musk",
                                "salience_score": 0.9259419441223145,
                                "sentence_indexes": [0],
                            },
                            {
                                "entity_type": "ORG",
                                "text": "Tesla",
                                "salience_score": 0.9259419441223145,
                                "sentence_indexes": [0],
                            },
                            {
                                "entity_type": "Pers",
                                "text": "Steve Jobs",
                                "salience_score": 0.9259419441223145,
                                "sentence_indexes": [2],
                            },
                            {
                                "entity_type": "ORG",
                                "text": "Apple",
                                "salience_score": 0.9259419441223145,
                                "sentence_indexes": [2],
                            },
                        ]},  # noqa
                    "parameters": {"lang": "en"},
                }
            },
            {
                'version': 1,
                'data': {
                    'identifier': None,
                    'namespace': 'entity-linking',
                    'attributes': {
                        'entities': [
                            {
                                'entity_type': 'Pers',
                                'text': 'Elon Musk',
                                'salience_score': 0.9259419441223145,
                                'sentence_indexes': [0],
                                'wiki_link': 'https://www.wikidata.org/wiki/Q317521',
                                'wiki_score': 0.9352254867553711
                            },
                            {
                                'entity_type': 'ORG',
                                'text': 'Tesla',
                                'salience_score': 0.9259419441223145,
                                'sentence_indexes': [0],
                                'wiki_link': 'https://www.wikidata.org/wiki/Q478214',
                                'wiki_score': 0.9614943265914917
                            },
                            {
                                'entity_type': 'Pers',
                                'text': 'Steve Jobs',
                                'salience_score': 0.9259419441223145,
                                'sentence_indexes': [2],
                                'wiki_link': 'https://www.wikidata.org/wiki/Q19837',
                                'wiki_score': 0.8936492800712585
                            },
                            {
                                'entity_type': 'ORG',
                                'text': 'Apple',
                                'salience_score': 0.9259419441223145,
                                'sentence_indexes': [2],
                                'wiki_link': 'https://www.wikidata.org/wiki/Q312',
                                'wiki_score': 0.9717069268226624
                            }
                        ]
                    }
                }
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