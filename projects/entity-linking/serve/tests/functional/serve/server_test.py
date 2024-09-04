"""Server functional tests."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


def test_model_server_liveness(test_client):
    """Tests the liveness endpoint of a running ModelServer instance."""
    liveness_response = test_client.get("/entity-linking/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().model_dump()


def test_model_server_readiness(test_client):
    """Tests the readiness endpoint of a running ModelServer instance."""
    readiness_response = test_client.get("/entity-linking/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().model_dump()


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "In the heart of Paris, one can find the enchanting Notre-Dame Cathedral, a masterpiece of French Gothic architecture. Built between 1163 and 1345, Notre-Dame has been a witness to many of the city's most significant historical events. It stands proudly on the Île de la Cité, surrounded by the Seine River, and its intricate façade and towering spires have captivated visitors for centuries. Not far from Notre-Dame, the Louvre Museum houses one of the most impressive art collections in the world. Originally a royal palace, the Louvre was transformed into a public museum during the French Revolution. It is now home to thousands of works of art, including the iconic Mona Lisa by Leonardo da Vinci. The museum's glass pyramid entrance, designed by architect I. M. Pei, is a modern contrast to the historical building and has become a symbol of the museum's commitment to both tradition and innovation. Paris is also renowned for its culinary scene, with countless bistros and cafés serving delicious French cuisine. The Eiffel Tower, an iron lattice tower constructed for the 1889 Exposition Universelle, offers breathtaking views of the city. Named after the engineer Gustave Eiffel, who designed it, the tower has become an enduring symbol of Paris and a must-see for anyone visiting the city. Whether exploring the art treasures of the Louvre, admiring the architectural grandeur of Notre-Dame, or enjoying a meal with a view of the Eiffel Tower, Paris offers an unforgettable experience that blends history, culture, and gastronomy.",
                        "entities": [
                            {
                                "entity_type": None,
                                "entity_text": "Paris",
                                "score": 0.4507485330104828,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Notre-Dame Cathedral",
                                "score": 0.8289842009544373,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Île de la Cité",
                                "score": 0.9111210703849792,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Seine River",
                                "score": 0.7985472083091736,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Louvre Museum",
                                "score": 0.8049250245094299,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": None,
                                "entity_text": "French Revolution",
                                "score": 0.7658177018165588,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Mona Lisa",
                                "score": 0.7146372199058533,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Leonardo da Vinci",
                                "score": 0.876043438911438,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": None,
                                "entity_text": "I. M. Pei",
                                "score": 0.5038636922836304,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": None,
                                "entity_text": "bistros",
                                "score": 0.2330305576324463,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": None,
                                "entity_text": "French cuisine",
                                "score": 0.21205313503742218,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Eiffel Tower",
                                "score": 0.8133144974708557,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q243",
                            },
                        ],
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
                                "entity_text": "Paris",
                                "score": 0.4507485330104828,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q90",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Notre-Dame Cathedral",
                                "score": 0.8289842009544373,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q2981",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Île de la Cité",
                                "score": 0.9111210703849792,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q190063",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Seine River",
                                "score": 0.7985472083091736,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q1471",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Louvre Museum",
                                "score": 0.8049250245094299,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q19675",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "French Revolution",
                                "score": 0.7658177018165588,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q6534",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Mona Lisa",
                                "score": 0.7146372199058533,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q12418",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Leonardo da Vinci",
                                "score": 0.876043438911438,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q762",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "I. M. Pei",
                                "score": 0.5038636922836304,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q46868",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "bistros",
                                "score": 0.2330305576324463,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q866742",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "French cuisine",
                                "score": 0.21205313503742218,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q6661",
                            },
                            {
                                "entity_type": None,
                                "entity_text": "Eiffel Tower",
                                "score": 0.8133144974708557,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q243",
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

    assert response.status_code == 204
    assert response.text == ""
