"""Feature registration utils."""

# Standard Library
import json
# from src.settings import PromptBackendAPISettings
from typing import Dict

# 3rd party libraries
import pandas as pd
import requests
from class_dict import CANDIDATE_DICT_FIRST


class PromptBackendAPISettings:  # OnclusiveBaseSettings is not serializable.
    # Placed in this file due to the circular import issue.
    """API configuration."""

    PROMPT_API: str = "http://prompt-backend:4000"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "1234"
    CLAUDE_IPTC_ALIAS: str = "ml-iptc-topic-prediction"

    IPTC_RESPONSE_SCHEMA: Dict[str, str] = {
        "iptc category": "Answer the IPTC category",
    }
    DEFAULT_MODEL: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"


settings = PromptBackendAPISettings()


def generate_label_llm(title, article, candidates):
    """Invoke LLM to generate IPTC ."""
    input_dict = {
        "input": {"title": title, "article": article, "candidates": candidates},
        "output": settings.IPTC_RESPONSE_SCHEMA,
    }
    headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}
    q = requests.post(
        "{}/api/v2/prompts/{}/generate/model/{}".format(
            settings.PROMPT_API, settings.CLAUDE_IPTC_ALIAS, settings.DEFAULT_MODEL
        ),
        headers=headers,
        json=input_dict,
    )
    output_content = json.loads(q.content)
    return output_content["iptc category"]


def iptc_first_level_on_demand_feature_view(features_df: pd.DataFrame) -> pd.DataFrame:
    """On-demand feature view transformation."""
    
    df = pd.DataFrame()
    topic_label = [
        generate_label_llm(title, content, CANDIDATE_DICT_FIRST)
        for title, content in zip(
            features_df["title"].values, features_df["content"].values
        )
    ]
    df["topic_1_llm"] = pd.Series(topic_label).astype(pd.StringDtype())
    return df
