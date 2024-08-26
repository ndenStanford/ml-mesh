"""Feature registration utils."""

# Standard Library
import asyncio
import json
# from src.settings import PromptBackendAPISettings
from typing import Dict

# 3rd party libraries
import aiohttp
import pandas as pd
import requests

# Source
from src.class_dict import CANDIDATE_DICT_FIRST, CANDIDATE_DICT_SECOND


class PromptBackendAPISettings:  # OnclusiveBaseSettings is not serializable.
    # Placed in this file due to the circular import issue.
    """API configuration."""

    PROMPT_API: str = "http://prompt-backend:4000"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "1234"
    CLAUDE_IPTC_ALIAS: str = "ml-iptc-topic-prediction"

    IPTC_RESPONSE_SCHEMA: Dict[str, str] = {
        "iptc category": "Answer the IPTC category",
    }
    DEFAULT_MODEL: str = "gpt-4o-mini"


settings = PromptBackendAPISettings()


def get_candidate_list(row, level):
    if level == 1:
        node_name = "root"
        candidate_list = list(
            CANDIDATE_DICT_FIRST.get(node_name, {"dummy": "dummy"}).values()
        )
    elif level == 2:
        node_name = row["topic_1"]
        candidate_list = list(
            CANDIDATE_DICT_SECOND.get(node_name, {"dummy": "dummy"}).values()
        )

    return candidate_list


def get_col_name(level):
    col_name = f"topic_{level}_llm"
    return col_name


async def generate_label_llm(row, session, level):
    """Invoke LLM to generate IPTC asynchronously."""

    candidate_list = get_candidate_list(row, level)

    input_dict = {
        "input": {
            "title": row["title"],
            "article": row["content"],
            "candidates": candidate_list,
        },
        "output": settings.IPTC_RESPONSE_SCHEMA,
    }
    headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

    async with session.post(
        "{}/api/v2/prompts/{}/generate/model/{}".format(
            settings.PROMPT_API, settings.CLAUDE_IPTC_ALIAS, settings.DEFAULT_MODEL
        ),
        headers=headers,
        json=input_dict,
    ) as response:
        output_content = await response.json()
        return output_content["iptc category"]


async def enrich_dataframe(features_df: pd.DataFrame, level) -> pd.DataFrame:
    """On-demand feature view transformation with async."""
    # Make a copy of the DataFrame to avoid modifying the original
    features_df_copy = features_df.copy()
    col_name = get_col_name(level)

    async with aiohttp.ClientSession() as session:
        tasks = [
            generate_label_llm(row, session, level)
            for _, row in features_df_copy.iterrows()
        ]
        features_df_copy[col_name] = await asyncio.gather(*tasks)
    return features_df_copy
# def iptc_on_demand_feature_view(features_df: pd.DataFrame) -> pd.DataFrame:
#     """Wrapper function to run the async enrichment."""
#     features_df_with_label = asyncio.run(enrich_dataframe(features_df))
#     df = pd.DataFrame()
#     col_name=get_col_name()
#     df[col_name] = features_df_with_label[col_name].astype(pd.StringDtype())
#     return df
def iptc_first_level_on_demand_feature_view(features_df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function to run the async enrichment."""
    level = 1
    features_df_with_label = asyncio.run(enrich_dataframe(features_df, level))

    df = pd.DataFrame()
    col_name = get_col_name(level)
    df[col_name] = features_df_with_label[col_name].astype(pd.StringDtype())
    return df


def iptc_second_level_on_demand_feature_view(features_df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function to run the async enrichment."""
    level = 2
    features_df_with_label = asyncio.run(enrich_dataframe(features_df, level))

    df = pd.DataFrame()
    col_name = get_col_name(level)
    df[col_name] = features_df_with_label[col_name].astype(pd.StringDtype())
    return df
