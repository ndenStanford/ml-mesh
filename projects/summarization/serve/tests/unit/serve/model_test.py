"""Model test."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest

# Source
from src.serve.model import SummarizationServedModel
from src.serve.schemas import PredictRequestSchema


# from pytest_unordered import unordered


def test_model_bio(summarization_model):
    """Model bio test."""
    assert summarization_model.bio().model_dump() == {
        "version": 2,
        "data": {
            "namespace": "summarization",
            "identifier": None,
            "attributes": {
                "model_name": "summarization",
                "model_card": {},
            },
        },
    }


@pytest.mark.parametrize(
    "text, desired_length, input_language, output_language, type, expected_summary",
    [
        (
            """Elon Musk was the second person ever to amass a personal fortune of more than $200 billion,
            breaching that threshold in January 2021, months after Jeff Bezos.""",
            100,
            "en",
            "en",
            "bespoke",
            """Elon Musk reached a net worth of over $200 billion in January 2021,
            becoming the second individual to achieve this milestone after Jeff Bezos.""",
        ),
    ],
)
@patch.object(SummarizationServedModel, "_inference")
def test_model_inefrence(
    mock_inference,
    summarization_model,
    text,
    desired_length,
    input_language,
    output_language,
    type,
    expected_summary,
):
    """Test model inference."""
    mock_inference.return_value = expected_summary

    summary = summarization_model._inference(
        text, desired_length, input_language, output_language, type
    )

    assert summary == expected_summary


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "namespace": "summarization",
                    "attributes": {
                        "content": """Elon Musk was the second person ever to amass a personal fortune of more than $200 billion,
                        breaching that threshold in January 2021, months after Jeff Bezos."""
                    },
                    "parameters": {
                        "input_language": "en",
                        "output_language": "en",
                        "summary_type": "",
                        "desired_length": 200,
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "summarization",
                    "attributes": {
                        "summary": """Elon Musk reached a net worth of over $200 billion
                        in January 2021, becoming the second individual to achieve this
                        milestone after Jeff Bezos."""
                    },
                },
            },
        )
    ],
)
@patch.object(SummarizationServedModel, "predict")
def test_model_predict(mock_predict, summarization_model, payload, expected_response):
    """Test model predict."""
    mock_predict.return_value = expected_response

    response = summarization_model.predict(PredictRequestSchema(**payload))

    mock_predict.assert_called_with(PredictRequestSchema(**payload))

    assert response == expected_response
