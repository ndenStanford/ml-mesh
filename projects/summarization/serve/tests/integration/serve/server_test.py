"""Model test."""

# 3rd party libraries
import pytest
from fastapi import status

# Internal libraries
from onclusiveml.nlp.language import LanguageIso


content = """
        Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos.
        The Tesla Isnc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth.
        Musk, 51, has seen his wealth plummet to $137 billion after Tesla shares tumbled in recent weeks, including an 11% drop on Tuesday, according to the Bloomberg Billionaires Index. His fortune peaked at $340 billion on Nov. 4, 2021, and he remained the world's richest person until he was overtaken this month by Bernard Arnault, the French tycoon behind luxury-goods powerhouse LVMH.
        The round-number milestone reflects just how high Musk soared during the run-up in asset prices during the easy-money pandemic era. Tesla exceeded a $1 trillion market capitalization for the first time in October 2021, joining the likes of ubiquitous technology companies Apple Inc., Microsoft Corp., Amazon.com Inc. and Google parent Alphabet Inc., even though its electric vehicles represented only a sliver of the overall auto market."""  # noqa: E501


@pytest.mark.parametrize(
    "payload",
    [
        {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": content},
                "parameters": {
                    "input_language": "en",
                    "output_language": "en",
                    "summary_type": "section",
                    "desired_length": 50,
                },
            }
        },
        {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": content},
                "parameters": {
                    "input_language": "en",
                    "output_language": "fr",
                    "summary_type": "section",
                    "desired_length": 100,
                },
            }
        },
    ],
)
def test_integration_summarization_model(test_client, payload):
    """Integration test for SummarizationServedModel."""
    response = test_client.post("/summarization/v2/predict", json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]["attributes"]["summary"]) > 0


@pytest.mark.parametrize(
    "payload",
    [
        {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": content},
                "parameters": {
                    "input_language": "hu",
                    "output_language": "en",
                    "summary_type": "bespoke",
                },
            }
        },
        {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": content},
                "parameters": {
                    "input_language": "hu",
                    "output_language": "hu",
                    "summary_type": "bespoke",
                    "desired_length": 100,
                },
            }
        },
    ],
)
def test_invalid_language(test_client, payload):
    """Test for invalid language."""
    response = test_client.post("/summarization/v2/predict", json=payload)
    print(response)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"] == (
        f"Summary language '{LanguageIso.from_language_iso(payload['data']['parameters']['input_language'])}' and or '{payload['data']['parameters']['summary_type']}' not supported."  # noqa: E501,W505
    )
