"""Model test."""

# 3rd party libraries
import pytest
from deepeval.dataset import EvaluationDataset
from fastapi import status

# Internal libraries
from onclusiveml.nlp.language import LanguageIso


content = """
        Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos.
        The Tesla Isnc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth.
        Musk, 51, has seen his wealth plummet to $137 billion after Tesla shares tumbled in recent weeks, including an 11% drop on Tuesday, according to the Bloomberg Billionaires Index. His fortune peaked at $340 billion on Nov. 4, 2021, and he remained the world's richest person until he was overtaken this month by Bernard Arnault, the French tycoon behind luxury-goods powerhouse LVMH.
        The round-number milestone reflects just how high Musk soared during the run-up in asset prices during the easy-money pandemic era. Tesla exceeded a $1 trillion market capitalization for the first time in October 2021, joining the likes of ubiquitous technology companies Apple Inc., Microsoft Corp., Amazon.com Inc. and Google parent Alphabet Inc., even though its electric vehicles represented only a sliver of the overall auto market."""  # noqa: E501

multi_article_content = [
    "The German Research Foundation (DFG) is a major research funding organization in Germany.",
    "In 2019, the DFG had a budget of €3.3 billion for research funding.",
]  # noqa: E501


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
                "attributes": {"content": multi_article_content},
                "parameters": {
                    "input_language": "en",
                    "output_language": "en",
                    "summary_type": "section",
                },
            }
        },
        {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": multi_article_content},
                "parameters": {
                    "input_language": "en",
                    "output_language": "en",
                    "summary_type": "bespoke",
                    "custom_instructions": [
                        "You are a scientific researcher.",
                        "I want the summary to have a neutral sentiment.",
                        "The tone should be formal.",
                        "Please remove any quoted text.",
                        "Use UK English spelling.",
                        "Apply sentence case capitalization.",
                        "Use the 24-hour time format.",
                        "Hyphenate compound words.",
                        "Use metric units for any measurements.",
                    ],
                },
            }
        },
    ],
)
def test_multi_article(test_client, payload):
    """Test for multi-article summarization."""
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
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"] == (
        f"Prompt not found. Summary language '{LanguageIso.from_language_iso(payload['data']['parameters']['input_language'])}' and or '{payload['data']['parameters']['summary_type']}' not supported."  # noqa: E501,W505
    )


@pytest.mark.parametrize(
    "payload",
    [
        {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": content},
                "parameters": {
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
                    "output_language": "fr",
                    "summary_type": "section",
                    "desired_length": 100,
                },
            }
        },
    ],
)
def test_no_input_language(test_client, payload):
    """Test when the input_language parameter is not provided."""
    response = test_client.post("/summarization/v2/predict", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]["attributes"]["summary"]) > 0


def test_prompt_evaluation(
    settings, test_client, test_df, test_df_path_enriched, metric
):
    """Test the prompt performance using LLM."""

    def enrich_row(row):
        content = row["content"]
        desired_length = len(content) // int(settings.SUMMARIZATION_COMPRESSION_RATIO)
        payload = {
            "data": {
                "namespace": "summarization",
                "attributes": {"content": content},
                "parameters": {
                    "output_language": "en",
                    "summary_type": "section",
                    "desired_length": desired_length,
                },
            }
        }
        response = test_client.post("/summarization/v2/predict", json=payload)
        return response.json()["data"]["attributes"]["summary"]

    test_df["summary"] = test_df.apply(enrich_row, axis=1)
    test_df.to_csv(test_df_path_enriched)

    dataset = EvaluationDataset()
    dataset.add_test_cases_from_csv_file(
        file_path=test_df_path_enriched,
        input_col_name="content",
        actual_output_col_name="summary",
    )

    result = dataset.evaluate([metric])
    percent_success = sum([r.success for r in result]) / len(result)
    assert percent_success > float(settings.PERCENT_SUCCESS)
