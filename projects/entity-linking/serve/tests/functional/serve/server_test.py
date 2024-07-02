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
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Apple",
                                "score": 0.999211311340332,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": "PER",
                                "entity_text": "Elon Musk",
                                "score": 0.9523038864135742,
                                "sentence_index": [2],
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Tesla",
                                "score": 0.9936597347259521,
                                "sentence_index": [2],
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
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "Die Olympischen Sommerspiele 2024 (französisch: Jeux olympiques d'été de 2024), offiziell die Spiele der XXXIII. Olympiade (französisch: Jeux de la XXXIIIe Olympiade) und allgemein bekannt als Paris 2024, sind ein bevorstehendes internationales Multisport-Ereignis, das vom 26. Juli bis zum 11. August 2024 in Frankreich stattfinden soll, mit Paris als Hauptaustragungsort und 16 weiteren Städten, die über das französische Mutterland verteilt sind, sowie einem Unteraustragungsort in Tahiti - einer Insel innerhalb des französischen Überseegebiets und der Überseekollektivität Französisch-Polynesien.",  # noqa
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "Die Olympischen Sommerspiele Spiele X",
                                "score": 0.9277721921602885,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": "MISC",
                                "entity_text": "Olympiade",
                                "score": 0.8323558866977692,
                                "sentence_index": [1],
                            },
                            {
                                "entity_type": "MISC",
                                "entity_text": "Je de la XX Olympiade",
                                "score": 0.9006950344358172,
                                "sentence_index": [1],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Paris",
                                "score": 0.9990205764770508,
                                "sentence_index": [1],
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Multisport",
                                "score": 0.8727646172046661,
                                "sentence_index": [1],
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Ereignis",
                                "score": 0.7371097579598427,
                                "sentence_index": [1],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Frankreich",
                                "score": 0.5097579459349314,
                                "sentence_index": [3],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Paris",
                                "score": 0.9968839287757874,
                                "sentence_index": [3],
                            },
                        ],
                    },
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
                                "entity_type": "MISC",
                                "entity_text": "Olympiade",
                                "score": 0.8323558866977692,
                                "sentence_index": [1],
                                "wiki_link": "https://www.wikidata.org/wiki/Q221956",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Paris",
                                "score": 0.9990205764770508,
                                "sentence_index": [1],
                                "wiki_link": "https://www.wikidata.org/wiki/Q90",
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Multisport",
                                "score": 0.8727646172046661,
                                "sentence_index": [1],
                                "wiki_link": "https://www.wikidata.org/wiki/Q167170",
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Ereignis",
                                "score": 0.7371097579598427,
                                "sentence_index": [1],
                                "wiki_link": "https://www.wikidata.org/wiki/Q167170",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Frankreich",
                                "score": 0.5097579459349314,
                                "sentence_index": [3],
                                "wiki_link": "https://www.wikidata.org/wiki/Q142",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Paris",
                                "score": 0.9968839287757874,
                                "sentence_index": [3],
                                "wiki_link": "https://www.wikidata.org/wiki/Q90",
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
                        "content": "ピョートル大帝は今日、最も強大な皇帝の一人と考えられている。ピョートル大帝は、全ヨーロッパに潜入した後、サンクトペテルブルクを建設した。モンゴル帝国との数世紀にわたる戦いの後、ロシアはついに西洋のルネサンスに追いついた。",  # noqa
                        "entities": [
                            {
                                "entity_type": "PER",
                                "entity_text": "ピョートル",
                                "score": 0.9994430939356486,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": "PER",
                                "entity_text": "ピョートル",
                                "score": 0.9992485443751017,
                                "sentence_index": [1],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "ヨーロッパ",
                                "score": 0.9485726952552795,
                                "sentence_index": [1],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "サンクトペテルブルク",
                                "score": 0.9998002648353577,
                                "sentence_index": [1],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "モンゴル",
                                "score": 0.9997795621554056,
                                "sentence_index": [2],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "ロシア",
                                "score": 0.9998742341995239,
                                "sentence_index": [2],
                            },
                        ],
                    },
                    "parameters": {"lang": "ja"},
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
                                "entity_text": "ピョートル",
                                "score": 0.9994430939356486,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q8479",
                            },
                            {
                                "entity_type": "PER",
                                "entity_text": "ピョートル",
                                "score": 0.9992485443751017,
                                "sentence_index": [1],
                                "wiki_link": "https://www.wikidata.org/wiki/Q8479",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "ヨーロッパ",
                                "score": 0.9485726952552795,
                                "sentence_index": [1],
                                "wiki_link": "https://www.wikidata.org/wiki/Q46",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "サンクトペテルブルク",
                                "score": 0.9998002648353577,
                                "sentence_index": [1],
                                "wiki_link": "https://www.wikidata.org/wiki/Q656",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "モンゴル",
                                "score": 0.9997795621554056,
                                "sentence_index": [2],
                                "wiki_link": "https://www.wikidata.org/wiki/Q12557",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "ロシア",
                                "score": 0.9998742341995239,
                                "sentence_index": [2],
                                "wiki_link": "https://www.wikidata.org/wiki/Q159",
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
                        "content": "Albert Einstein è considerato uno dei più grandi fisici di tutti i tempi. Anche se il suo lavoro si basava su quello di Plank e su altri risultati, ha rivoluzionato il mondo della fisica in un'epoca in cui si pensava che la scienza fosse completamente conosciuta. Questo portò anche gli Stati Uniti sulla strada del progetto Manhattan.",  # noqa
                        "entities": [
                            {
                                "entity_type": "PER",
                                "entity_text": "Albert Einstein",
                                "score": 0.9796470701694489,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": "PER",
                                "entity_text": "Plank",
                                "score": 0.8112821578979492,
                                "sentence_index": [1],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Stati Uniti",
                                "score": 0.8701310634613037,
                                "sentence_index": [2],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Manhattan",
                                "score": 0.5701310634613037,
                                "sentence_index": [2],
                            },
                        ],
                    },
                    "parameters": {"lang": "it"},
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
                                "entity_text": "Albert Einstein",
                                "score": 0.9796470701694489,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q937",
                            },
                            {
                                "entity_type": "PER",
                                "entity_text": "Plank",
                                "score": 0.8112821578979492,
                                "sentence_index": [1],
                                "wiki_link": "https://www.wikidata.org/wiki/Q9021",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Stati Uniti",
                                "score": 0.8701310634613038,
                                "sentence_index": [2],
                                "wiki_link": "https://www.wikidata.org/wiki/Q30",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Manhattan",
                                "score": 0.5701310634613037,
                                "sentence_index": [2],
                                "wiki_link": "https://www.wikidata.org/wiki/Q127050",
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
