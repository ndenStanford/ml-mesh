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
        (
            {
                "data": {
                    "identifier": "None",
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "NOAA says Earth's oceans becoming more acidic\n\n\u00a0\n\nAccording by the National Oceanic and Atmospheric Administration's  National Oceanic and Atmospheric Administration's National Oceanic and Atmospheric Administration's National Oceanic and Atmospheric Administration's National Oceanic and Atmospheric Administration's National Oceanic and Atmospheric Administration's (NOAA) Pacific Marine Environmental Laboratory, the level of acid in the world's oceans is rising, decades before scientists expected the levels to rise.\n\nThe study was performed on the coastal waters of the Pacific Ocean from Baja California, Mexico to Vancouver, British Columbia, where tests showed that acid levels in some areas near the edge of the Continental Shelf were high enough to corrode the shells of some sea creatures as well as some corals. Some areas showed excessive levels of acid less than  coastline in the United States.\n\n\"What we found ... was truly astonishing. This means ocean acidification may be seriously impacting marine life on the continental shelf right now. The models suggested they wouldn't be corrosive at the surface until sometime during the second half of this century,\" said Richard A. Feely, an oceanographer from the NOAA.\n\nThe natural processes of the seas and oceans constantly clean the Earth's air, absorbing 1/3 to 1/2 of the carbon dioxide generated by humans. As the oceans absorb more of the gas, the water becomes more acidic, reducing the amount of carbonate which shellfish such as clams and oysters use to form their shells, and increasing the levels of carbonic acid. Although levels are high, they are not yet high enough to threaten humans directly.\n\n\"Scientists have also seen a reduced ability of marine algae and free-floating plants and animals to produce protective carbonate shells,\" added Feely.\n\nFeely noted that, according to the study, the oceans and seas have absorbed more than 525 billion tons of carbon dioxide since the Industrial Revolution began.",  # noqa
                        "entities": [
                            {
                                "entity_type": None,
                                "entity_text": "carbon dioxide",
                                "score": 1.0,
                                "sentence_index": [4],
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
                                "entity_type": None,
                                "entity_text": "carbon dioxide",
                                "score": 1.0,
                                "sentence_index": [4],
                                "wiki_link": "https://www.wikidata.org/wiki/Q1997",
                            }
                        ]
                    },
                },
            },
        ),
        (
            {
                "data": {
                    "identifier": "de-72969",
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": (
                            "Saudischer Kronprinz Naif ibn Abd al-Aziz gestorben Riad (Saudi-Arabien), 17.06.2012 – Der saudische Thronfolger Naif ibn Abd al-Aziz ist tot. Der 78-jährige seit 1975 amtierende Innenminister und Halbbruder von König Abdullah starb in der Schweiz, wo er sich zur Krankenbehandlung aufhielt. An welcher gesundheitlichen Beeinträchtigung der Prinz litt, ist nicht bekannt. Naif hatte im Oktober seinen an Krebs verstorbenen Bruder Sultan ibn Abd al-Aziz abgelöst. Das politische Vermächtnis von Prinz Naif wird unterschiedlich beurteilt. Als Verdienst rechnet man ihm sein kompromissloses Vorgehen gegen das Terroristennetzwerk al-Qaida an, als er zwischen 2003 und 2008 deren Zellen in Saudi-Arabien zerschlug. Doch Kritiker werfen ihm die Unterdrückung der Opposition im Lande vor. Auch von Frauenrechtlerinnen wurde der verstorbene Kronprinz kritisiert, weil er gegen die Forderungen der saudi-arabischen Frauen gewesen sei, alleine Autofahren zu dürfen. Außerdem habe er die Reformversuche des 87-jährigen Königs Abdullah behindert, etwa bei der Einführung des Wahlrechts für Frauen bei Kommunalwahlen. Nun wird zum zweiten Mal innerhalb eines Jahres nach einem Thronfolger für den 87-jährigen Herrscher gesucht. Dabei wurde von Beobachtern der 76 Jahre alte derzeitige Verteidigungsminister Salman ibn Abd al-Aziz als Favorit genannt. Der frühere Gouverneur von Riad gilt als eher aufgeschlossen für Reformen. Die Thronfolge ist in Saudi-Arabien, im Gegensatz zu Königshäusern in Europa, nicht festgelegt. Der jeweilige Thronfolger wird von einem Familiengremium bestimmt. Dieses wird als neuen Thronfolger einen der etwa zwanzig noch lebenden Söhne des Staatsgründers Ibn Saud auswählen. König Ibn Saud starb 1953, und ihm folgten seitdem fünf seiner Söhne auf den Thron. Die Beerdigung Naif ibn Abd al-Aziz' ist für den 17.06.2012 in Mekka vorgesehen. König Abdullah ist hierzu bereits in Mekka eingetroffen."  # noqa
                        ),
                        "entities": [
                            {
                                "entity_type": "LOC",
                                "entity_text": "Saudi-Arabien",
                                "score": 1.0,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Naif ibn Abd al-Aziz",
                                "score": 1.0,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Salman ibn Abd al-Aziz",
                                "score": 1.0,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Ibn Saud",
                                "score": 1.0,
                                "sentence_index": [0],
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Mekka",
                                "score": 1.0,
                                "sentence_index": [0],
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
                                "entity_type": "LOC",
                                "entity_text": "Saudi-Arabien",
                                "score": 1.0,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q851",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Naif ibn Abd al-Aziz",
                                "score": 1.0,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q317832",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Salman ibn Abd al-Aziz",
                                "score": 1.0,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q367825",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Ibn Saud",
                                "score": 1.0,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q151509",
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "Mekka",
                                "score": 1.0,
                                "sentence_index": [0],
                                "wiki_link": "https://www.wikidata.org/wiki/Q5806",
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
