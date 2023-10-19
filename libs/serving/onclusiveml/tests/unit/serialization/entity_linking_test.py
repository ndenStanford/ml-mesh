"""Entity linking schemas test."""

# 3rd party libraries
import pytest
from pydantic import ValidationError

# Internal libraries
from onclusiveml.serving.serialization.entity_linking.v1 import (
    PredictRequestAttributeSchemaV1,
    PredictRequestParametersSchemaV1,
    PredictResponseAttributeSchemaV1,
    PredictResponseEntity,
)


@pytest.mark.parametrize(
    "content",
    [
        "test content",
        "test content 2",
    ],
)
def test_request_schema_attributes(content):
    """Test request schema attributes."""
    attributes = PredictRequestAttributeSchemaV1(content=content)

    assert attributes.content == content
    assert isinstance(attributes.content, str)
    assert dict(attributes) == {"content": content}


def test_request_schema_attributes_extra():
    """Test request schema attributes with extra parameter."""
    with pytest.raises(ValidationError):
        _ = PredictRequestAttributeSchemaV1(content="content", extra="")


@pytest.mark.parametrize("lang", ["en", "fr"])
def test_request_schema_parameters(lang):
    """Test request schema parameters."""
    parameters = PredictRequestParametersSchemaV1(lang=lang)

    assert parameters.lang == lang
    assert isinstance(parameters.lang, str)
    assert dict(parameters) == {"lang": lang}


def test_request_schema_parameters_extra():
    """Test request schema attributes with extra parameter."""
    with pytest.raises(ValidationError):
        _ = PredictRequestParametersSchemaV1(extra="")


@pytest.mark.parametrize(
    "entity_type, entity_text, score, sentence_index, wiki_link",
    [("ORG", "Company name", 0.9, 0, "link")],
)
def test_response_attribute_schema(
    entity_type, entity_text, score, sentence_index, wiki_link
):
    """Test response schema parameters."""
    attributes = PredictResponseAttributeSchemaV1(
        entities=[
            PredictResponseEntity(
                entity_type=entity_type,
                entity_text=entity_text,
                score=score,
                sentence_index=sentence_index,
                wiki_link=wiki_link,
            )
        ]
    )

    assert attributes.entities[0].entity_type == entity_type
    assert attributes.entities[0].entity_text == entity_text
    assert attributes.entities[0].score == score
    assert attributes.entities[0].sentence_index == sentence_index
    assert attributes.entities[0].wiki_link == wiki_link

    assert isinstance(attributes.entities[0].entity_type, str)
    assert isinstance(attributes.entities[0].entity_text, str)
    assert isinstance(attributes.entities[0].score, float)
    assert isinstance(attributes.entities[0].sentence_index, int)
    assert isinstance(attributes.entities[0].wiki_link, str)

    assert dict(attributes) == {
        "entities": [
            {
                "entity_type": entity_type,
                "entity_text": entity_text,
                "score": score,
                "sentence_index": sentence_index,
                "wiki_link": wiki_link,
            }
        ]
    }


def test_request_request_attributes_extra():
    """Test request schema attributes with extra parameter."""
    with pytest.raises(ValidationError):
        _ = PredictRequestParametersSchemaV1(extra="")
