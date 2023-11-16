"""IPTC schemas test."""

# 3rd party libraries
import pytest
from pydantic import ValidationError

# Internal libraries
from onclusiveml.serving.serialization.iptc.v1 import (
    PredictRequestAttributeSchemaV1,
    PredictRequestParametersSchemaV1,
    PredictResponseAttributeSchemaV1,
    PredictResponseIPTC,
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


@pytest.mark.parametrize(
    "label, score",
    [("economy, business and finance", 0.9870238304138184)],
)
def test_response_attribute_schema(label, score):
    """Test response schema parameters."""
    attributes = PredictResponseAttributeSchemaV1(
        iptc=PredictResponseIPTC(
            label="economy, business and finance", score=0.9870238304138184
        )
    )

    assert attributes.iptc[0].label == label
    assert attributes.iptc[0].score == score

    assert isinstance(attributes.iptc[0].label, str)
    assert isinstance(attributes.iptc[0].score, float)

    assert dict(attributes) == {"iptc": [{"label": label, "score": score}]}


def test_request_request_attributes_extra():
    """Test request schema attributes with extra parameter."""
    with pytest.raises(ValidationError):
        _ = PredictRequestParametersSchemaV1(extra="")
