"""Model test."""

# 3rd party libraries
import pytest


@pytest.mark.parametrize(
    "query",
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
            }
        )
    ],
)
def test__query_wiki(entity_linking_model, query):
    """Test query wiki."""
    result = entity_linking_model._query_wiki(query)

    assert result["software"] == "entity-fishing"
    assert isinstance(result["runtime"], int)
    assert isinstance(result["nbest"], bool)
    assert result["text"] == query["text"]
    assert result["language"]["lang"] == query["language"]["lang"]
    # assert isinstance(result["entities"], list)


@pytest.mark.parametrize(
    "content",
    [
        "Meta AI has been announced, and it’s coming to Messenger.",
        "Google AI is a division of Google dedicated to artificial intelligence.",
    ],
)
def test__get_entity_linking(entity_linking_model, content):
    """Test entity linking query."""
    result = entity_linking_model._get_entity_linking(content)

    assert isinstance(result, list)


@pytest.mark.parametrize(
    "content,language",
    [
        ("Meta AI has been announced, and it’s coming to Messenger.", "en"),
        # "Google AI is a division of Google dedicated to artificial intelligence.","en"
    ],
)
def test__predict(entity_linking_model, content, language):
    """Test _predict method."""
    result = entity_linking_model._predict(content=content, language=language)

    assert isinstance(result, list)
