"""Model test."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
from pytest_unordered import unordered

# Source
from src.serve.model import EntityLinkingServedModel
from src.serve.schemas import PredictRequestSchema


def test_model_bio(entity_linking_model):
    """Model bio test."""
    assert entity_linking_model.bio().dict() == {
        "version": 1,
        "data": {
            "namespace": "entity-linking",
            "identifier": None,
            "attributes": {
                "model_name": "entity-linking",
            },
        },
    }


def test_model_headers(entity_linking_model):
    """Test model headers."""
    assert entity_linking_model.headers == {"x-api-key": ""}


@pytest.mark.parametrize(
    "payload, predict_return, expected_response",
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
            [],
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
            [
                {
                    "entity_type": "ORG",
                    "entity_text": "Tottenham Hotspur Football Club",
                    "score": 0.9259419441223145,
                    "sentence_index": 0,
                    "wiki_link": "https://www.wikidata.org/wiki/Q18741",
                }
            ],
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
                                "sentence_index": 0,
                            }
                        ],
                    },
                    "parameters": {"lang": "en"},
                }
            },
            [
                {
                    "entity_type": "ORG",
                    "entity_text": "Tottenham Hotspur Football Club",
                    "score": 0.9259419441223145,
                    "sentence_index": 0,
                    "wiki_link": "https://www.wikidata.org/wiki/Q18741",
                }
            ],
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
    ],
)
@patch.object(EntityLinkingServedModel, "_predict")
def test_model_predict(
    mock_predict, entity_linking_model, payload, predict_return, expected_response
):
    """Test model predict."""
    mock_predict.return_value = predict_return

    attributes = payload["data"]["attributes"]
    parameters = payload["data"]["parameters"]

    response = entity_linking_model.predict(PredictRequestSchema(**payload))

    entities = attributes.get("entities", None)

    mock_predict.assert_called_with(attributes["content"], parameters["lang"], entities)

    assert response == expected_response


@pytest.mark.parametrize(
    "content, lang, entities, expected",
    [
        (
            "Although inflation has come down from the peak reached last year, it is still too high.",  # noqa
            "en",
            [],
            {
                "text": "Although inflation has come down from the peak reached last year, it is still too high.",  # noqa
                "language": {"lang": "en"},
                "mentions": [],
                "entities": [],
                "nbest": False,
                "sentence": False,
            },
        ),
        (
            "Chelsea agree to buy land next to Stamford Bridge for stadium rebuild",
            "en",
            [
                {
                    "entity_type": "ORG",
                    "entity_text": "Chelsea",
                    "score": 0.9987567663192749,
                    "sentence_index": 0,
                    "start": 0,
                    "end": 7,
                },
                {
                    "entity_type": "LOC",
                    "entity_text": "Stamford Bridge",
                    "score": 0.9972361624240875,
                    "sentence_index": 0,
                    "start": 34,
                    "end": 49,
                },
            ],
            {
                "text": "Chelsea agree to buy land next to Stamford Bridge for stadium rebuild",
                "language": {"lang": "en"},
                "mentions": [],
                "entities": [
                    {"rawName": "Stamford Bridge", "offsetStart": 34, "offsetEnd": 49},
                    {"rawName": "Chelsea", "offsetStart": 0, "offsetEnd": 7},
                ],
                "nbest": False,
                "sentence": False,
            },
        ),
    ],
)
def test_model__generate_query(entity_linking_model, content, lang, entities, expected):
    """Test generate query."""
    assert (
        entity_linking_model._generate_query(content, lang, entities)["text"]
        == expected["text"]
    )
    assert (
        entity_linking_model._generate_query(content, lang, entities)["language"]
        == expected["language"]
    )
    assert (
        entity_linking_model._generate_query(content, lang, entities)["mentions"]
        == expected["mentions"]
    )
    assert entity_linking_model._generate_query(content, lang, entities)[
        "entities"
    ] == unordered(expected["entities"])
    assert (
        entity_linking_model._generate_query(content, lang, entities)["nbest"]
        == expected["nbest"]
    )
    assert (
        entity_linking_model._generate_query(content, lang, entities)["sentence"]
        == expected["sentence"]
    )


@pytest.mark.parametrize(
    "query, expected",
    [
        (
            {
                "text": "Apple boosts UK hiring with AI-focused Cambridge office.",
                "language": {"lang": "en"},
                "mentions": [],
                "entities": [
                    {"rawName": "Apple", "offsetStart": 0, "offsetEnd": 5},
                    {"rawName": "UK", "offsetStart": 13, "offsetEnd": 15},
                    {"rawName": "AI", "offsetStart": 28, "offsetEnd": 30},
                    {"rawName": "Cambridge", "offsetStart": 39, "offsetEnd": 48},
                ],
                "nbest": False,
                "sentence": False,
            },
            {
                "software": "entity-fishing",
                "version": "N/A",
                "date": "2023-10-01T20:35:45.621Z",
                "runtime": 916,
                "nbest": False,
                "text": "Apple boosts UK hiring with AI-focused Cambridge office.",
                "language": {"lang": "en", "conf": 1.0},
                "entities": [
                    {
                        "rawName": "Apple",
                        "offsetStart": 0,
                        "offsetEnd": 5,
                        "confidence_score": 0.4386,
                        "wikipediaExternalRef": 856,
                        "wikidataId": "Q312",
                        "domains": ["Optics", "Electronics"],
                    },
                    {
                        "rawName": "UK",
                        "offsetStart": 13,
                        "offsetEnd": 15,
                        "confidence_score": 0.414,
                        "wikipediaExternalRef": 31717,
                        "wikidataId": "Q145",
                        "domains": ["Geology"],
                    },
                    {
                        "rawName": "AI",
                        "offsetStart": 28,
                        "offsetEnd": 30,
                        "confidence_score": 0.452,
                        "wikipediaExternalRef": 1654769,
                        "wikidataId": "Q2494121",
                        "domains": ["Computer_Science"],
                    },
                    {
                        "rawName": "Cambridge",
                        "offsetStart": 39,
                        "offsetEnd": 48,
                        "confidence_score": 0.4252,
                        "wikipediaExternalRef": 36995,
                        "wikidataId": "Q350",
                        "domains": ["Geography"],
                    },
                ],
            },
        )
    ],
)
@patch("requests.post")
def test_model__query_wiki(
    mock_entity_fishing_post, settings, entity_linking_model, query, expected
):
    """Test query wiki method."""
    mock_entity_fishing_post.return_value.json.return_value = expected

    entity_linking_model._query_wiki(query=query)

    mock_entity_fishing_post.assert_called_with(
        settings.entity_fishing_endpoint,
        json=query,
        headers={
            settings.api_key_name: settings.internal_ml_api_key.get_secret_value()
        },
    )


@pytest.mark.parametrize(
    "content, ner_response, entity_fishing_response, expected",
    [
        (
            "Meta AI has been announced, and it’s coming to Messenger.",
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "Meta AI",
                                "score": 0.9577947457631429,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 7,
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Messenger",
                                "score": 0.9432488083839417,
                                "sentence_index": 0,
                                "start": 47,
                                "end": 56,
                            },
                        ]
                    },
                },
            },
            {
                "software": "entity-fishing",
                "version": "N/A",
                "date": "2023-10-01T19:40:39.666Z",
                "runtime": 8,
                "nbest": False,
                "text": "Meta AI has been announced, and it’s coming to Messenger.",
                "language": {"lang": "en", "conf": 1.0},
                "entities": [
                    {
                        "rawName": "Messenger",
                        "offsetStart": 47,
                        "offsetEnd": 56,
                        "confidence_score": 0.3574,
                        "wikipediaExternalRef": 36250682,
                        "wikidataId": "Q116947",
                        "domains": [
                            "Electronics",
                            "Computer_Science",
                            "Telecommunication",
                        ],
                    }
                ],
            },
            [
                {
                    "entity_type": "ORG",
                    "entity_text": "Meta AI",
                    "score": 0.9577947457631429,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "ORG",
                    "entity_text": "Messenger",
                    "score": 0.9432488083839417,
                    "sentence_index": 0,
                    "wiki_link": "https://www.wikidata.org/wiki/Q116947",
                },
            ],
        ),
        (
            "Google AI is a division of Google dedicated to artificial intelligence.",
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "Google AI",
                                "score": 0.9856193959712982,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 9,
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "Google",
                                "score": 0.9987095594406128,
                                "sentence_index": 0,
                                "start": 27,
                                "end": 33,
                            },
                        ]
                    },
                },
            },
            {
                "software": "entity-fishing",
                "version": "N/A",
                "date": "2023-10-01T19:20:20.819Z",
                "runtime": 914,
                "nbest": False,
                "text": "Google AI is a division of Google dedicated to artificial intelligence.",
                "language": {"lang": "en", "conf": 1.0},
                "global_categories": [
                    {
                        "weight": 0.09090909090909091,
                        "source": "wikipedia-en",
                        "category": "Computer-related introductions in 1997",
                        "page_id": 51880327,
                    },
                    {
                        "weight": 0.09090909090909091,
                        "source": "wikipedia-en",
                        "category": "Websites which mirror Wikipedia",
                        "page_id": 11712915,
                    },
                    {
                        "weight": 0.09090909090909091,
                        "source": "wikipedia-en",
                        "category": "1997 establishments in the United States",
                        "page_id": 28378450,
                    },
                    {
                        "weight": 0.09090909090909091,
                        "source": "wikipedia-en",
                        "category": "Internet properties established in 1997",
                        "page_id": 13678260,
                    },
                    {
                        "weight": 0.09090909090909091,
                        "source": "wikipedia-en",
                        "category": "Alphabet Inc.",
                        "page_id": 47562417,
                    },
                    {
                        "weight": 0.09090909090909091,
                        "source": "wikipedia-en",
                        "category": "Multilingual websites",
                        "page_id": 15899220,
                    },
                    {
                        "weight": 0.09090909090909091,
                        "source": "wikipedia-en",
                        "category": "Artificial intelligence",
                        "page_id": 700355,
                    },
                    {
                        "weight": 0.09090909090909091,
                        "source": "wikipedia-en",
                        "category": "Google",
                        "page_id": 853521,
                    },
                    {
                        "weight": 0.09090909090909091,
                        "source": "wikipedia-en",
                        "category": "Google Search",
                        "page_id": 44575396,
                    },
                    {
                        "weight": 0.09090909090909091,
                        "source": "wikipedia-en",
                        "category": "Internet search engines",
                        "page_id": 699876,
                    },
                    {
                        "weight": 0.09090909090909091,
                        "source": "wikipedia-en",
                        "category": "Google services",
                        "page_id": 6090339,
                    },
                ],
                "entities": [
                    {
                        "rawName": "Google AI",
                        "offsetStart": 0,
                        "offsetEnd": 9,
                        "confidence_score": 0.898,
                        "wikipediaExternalRef": 54073206,
                        "wikidataId": "Q30688088",
                        "domains": ["Medicine"],
                    },
                    {
                        "rawName": "Google",
                        "offsetStart": 27,
                        "offsetEnd": 33,
                        "confidence_score": 0.8002,
                        "wikipediaExternalRef": 12431,
                        "wikidataId": "Q9366",
                        "domains": ["Electronics", "Computer_Science"],
                    },
                ],
            },
            [
                {
                    "entity_type": "ORG",
                    "entity_text": "Google AI",
                    "score": 0.9856193959712982,
                    "sentence_index": 0,
                    "wiki_link": "https://www.wikidata.org/wiki/Q30688088",
                },
                {
                    "entity_type": "ORG",
                    "entity_text": "Google",
                    "score": 0.9987095594406128,
                    "sentence_index": 0,
                    "wiki_link": "https://www.wikidata.org/wiki/Q30688088",
                },
            ],
        ),
    ],
)
@patch.object(EntityLinkingServedModel, "_query_wiki")
@patch("requests.post")
def test_model__get_entity_linking(
    mock_ner_post,
    mock_query_wiki,
    entity_linking_model,
    settings,
    content,
    ner_response,
    entity_fishing_response,
    expected,
):
    """Test get entity linking method."""
    mock_ner_post.return_value.json.return_value = ner_response
    mock_query_wiki.return_value = entity_fishing_response
    assert entity_linking_model._get_entity_linking(content) == expected

    mock_ner_post.assert_called_with(
        settings.entity_recognition_endpoint,
        json={
            "data": {
                "identifier": "string",
                "namespace": "ner",
                "attributes": {
                    "content": content,
                },
                "parameters": {"language": "en"},
            }
        },
    )

    mock_query_wiki.assert_called_once()


@pytest.mark.parametrize(
    "text, entities, expected",
    [
        (
            "AI",
            [
                {
                    "rawName": "AI",
                    "offsetStart": 45,
                    "offsetEnd": 47,
                    "confidence_score": 0.452,
                    "wikipediaExternalRef": 1654769,
                    "wikidataId": "Q2494121",
                    "domains": ["Computer_Science"],
                },
            ],
            "Q2494121",
        )
    ],
)
def test__get_wiki_id(entity_linking_model, text, entities, expected):
    """Test get wiki id method."""
    assert entity_linking_model._get_wiki_id(text, entities) == expected


@pytest.mark.parametrize(
    "text, entities, expected",
    [
        (
            "OpenAI code interpreter operates using a technology that harnesses the power of AI",
            [
                {
                    "entity_type": "ORG",
                    "entity_text": "OpenAI",
                    "score": 0.7062258124351501,
                    "sentence_index": 0,
                    "start": 0,
                    "end": 6,
                },
                {
                    "entity_type": "MISC",
                    "entity_text": "AI",
                    "score": 0.8235802054405212,
                    "sentence_index": 0,
                    "start": 80,
                    "end": 82,
                },
            ],
            [
                {"rawName": "OpenAI", "offsetStart": 0, "offsetEnd": 6},
                {"rawName": "AI", "offsetStart": 4, "offsetEnd": 6},
                {"rawName": "AI", "offsetStart": 80, "offsetEnd": 82},
            ],
        ),
        (
            "Amazon steps up AI race with up to 4 billion deal to invest in Anthropic",
            [
                {
                    "entity_type": "LOC",
                    "entity_text": "Amazon",
                    "score": 0.9809881448745728,
                    "sentence_index": 0,
                    "start": 0,
                    "end": 6,
                },
                {
                    "entity_type": "MISC",
                    "entity_text": "AI",
                    "score": 0.9847040176391602,
                    "sentence_index": 0,
                    "start": 16,
                    "end": 18,
                },
                {
                    "entity_type": "MISC",
                    "entity_text": "Anthropic",
                    "score": 0.9091429511706034,
                    "sentence_index": 0,
                    "start": 63,
                    "end": 72,
                },
            ],
            [
                {"rawName": "Amazon", "offsetStart": 0, "offsetEnd": 6},
                {"rawName": "Anthropic", "offsetStart": 63, "offsetEnd": 72},
                {"rawName": "AI", "offsetStart": 16, "offsetEnd": 18},
            ],
        ),
    ],
)
def test__generate_entity_query(entity_linking_model, text, entities, expected):
    """Test entity fishing query generation method."""
    assert entity_linking_model._generate_entity_query(text, entities) == unordered(
        expected
    )


@pytest.mark.parametrize(
    "entity, expected",
    [
        (
            {
                "entity_type": "ORG",
                "entity_text": "Google",
                "score": 0.9492171406745911,
                "sentence_index": 0,
                "wiki_link": "https://www.wikidata.org/wiki/Q95",
            },
            "Google",
        ),
        (
            {
                "entity_type": "ORG",
                "entity_text": "OpenAI",
                "score": 0.7062258124351501,
                "sentence_index": 0,
                "wiki_link": "https://www.wikidata.org/wiki/Q2494121",
            },
            "OpenAI",
        ),
        (
            {
                "entity_type": "MISC",
                "entity_text": "AI",
                "score": 0.8235802054405212,
                "sentence_index": 0,
                "wiki_link": "https://www.wikidata.org/wiki/Q2494121",
            },
            "AI",
        ),
    ],
)
def test__get_entity_text(entity_linking_model, entity, expected):
    """Test get entity text method."""
    assert entity_linking_model._get_entity_text(entity)
