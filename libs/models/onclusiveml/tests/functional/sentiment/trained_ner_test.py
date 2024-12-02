"""Functional Tests."""

# ML libs
import torch

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture


@pytest.mark.parametrize(
    "trained_sentiment_instance, test_document, device",
    [
        (
            lazy_fixture("trained_sentiment_instance"),
            lazy_fixture("test_document"),
            "cuda" if torch.cuda.is_available() else "cpu",
        ),
    ],
)
def test_inference_global_sentiment(trained_sentiment_instance, test_document, device):
    """Test global sentiment inference."""
    output = trained_sentiment_instance.inference(
        text=test_document, entities=None, window_length=500, device=device
    )

    assert isinstance(output, dict)
    assert "label" in output
    assert output["label"] in ["positive", "neutral", "negative"]
    assert "positive_prob" in output
    assert "negative_prob" in output


@pytest.mark.parametrize(
    "trained_sentiment_instance, test_document, device",
    [
        (
            lazy_fixture("trained_sentiment_instance"),
            lazy_fixture("test_document"),
            "cuda" if torch.cuda.is_available() else "cpu",
        ),
    ],
)
def test_inference_entity_sentiment(trained_sentiment_instance, test_document, device):
    """Test entity-specific sentiment inference."""
    entities = [
        {"entity_text": "Steven Paul Jobs"},
        {"entity_text": "Apple"},
    ]

    output = trained_sentiment_instance.inference(
        text=test_document, entities=entities, window_length=500, device=device
    )

    assert isinstance(output, dict)
    assert "entities" in output
    for entity in output["entities"]:
        assert "sentiment" in entity
        assert entity["sentiment"] in ["positive", "neutral", "negative"]
