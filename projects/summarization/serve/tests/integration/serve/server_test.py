"""Model test."""

# 3rd party libraries
import pytest
from fastapi import status


input = """
        Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos.
        The Tesla Isnc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth.
        Musk, 51, has seen his wealth plummet to $137 billion after Tesla shares tumbled in recent weeks, including an 11% drop on Tuesday, according to the Bloomberg Billionaires Index. His fortune peaked at $340 billion on Nov. 4, 2021, and he remained the world's richest person until he was overtaken this month by Bernard Arnault, the French tycoon behind luxury-goods powerhouse LVMH.
        The round-number milestone reflects just how high Musk soared during the run-up in asset prices during the easy-money pandemic era. Tesla exceeded a $1 trillion market capitalization for the first time in October 2021, joining the likes of ubiquitous technology companies Apple Inc., Microsoft Corp., Amazon.com Inc. and Google parent Alphabet Inc., even though its electric vehicles represented only a sliver of the overall auto market."""  # noqa: E501


def test_get_model_server(test_client):
    """Integration test for the get_model_server function."""
    response = test_client.get("/summarization/v1/")

    assert response.status_code == 200


@pytest.mark.parametrize(
    "payload",
    [
        {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": input},
                "parameters": {
                    "language": "en",
                    "target_language": "en",
                    "desired_length": 50,
                },
            }
        },
        {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": input},
                "parameters": {
                    "language": "en",
                    "target_language": "fr",
                    "desired_length": 100,
                },
            }
        },
    ],
)
def test_integration_summarization_model(test_client, payload):
    """Integration test for SummarizationServedModel."""
    response = test_client.post("/summarization/v1/predict", json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.model_dump_json()["data"]["attributes"]["summary"]) > 0


@pytest.mark.parametrize(
    "payload",
    [
        {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": input},
                "parameters": {
                    "language": "hu",
                    "target_language": "en",
                    "desired_length": 100,
                },
            }
        },
        {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": input},
                "parameters": {
                    "language": "en",
                    "target_language": "hu",
                    "desired_length": 200,
                },
            }
        },
        {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": input},
                "parameters": {
                    "language": "hu",
                    "target_language": "hu",
                    "desired_length": 100,
                },
            }
        },
    ],
)
def test_invalid_language(test_client, payload):
    """Test for invalid language."""
    response = test_client.post("/summarization/v1/predict", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.model_dump_json()["detail"] == "Unsupported language"
