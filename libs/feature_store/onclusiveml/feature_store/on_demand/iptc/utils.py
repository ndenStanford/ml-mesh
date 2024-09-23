# isort: skip_file
"""Feature registration utils."""

# Standard Library
import asyncio
import json

# from src.settings import PromptBackendAPISettings
from typing import Dict

# 3rd party libraries
import aiohttp
import pandas as pd

# Internal libraries
from onclusiveml.feature_store.on_demand.iptc.class_dict import (
    CANDIDATE_DICT_FIRST,
    CANDIDATE_DICT_SECOND,
    CANDIDATE_DICT_THIRD,
    CANDIDATE_DICT_FOURTH,
)
from onclusiveml.feature_store.on_demand.iptc.name_mapping_dict import (
    NAME_MAPPING_DICT_FIRST,
    NAME_MAPPING_DICT_SECOND,
    NAME_MAPPING_DICT_THIRD,
)


class PromptBackendAPISettings:  # OnclusiveBaseSettings is not serializable.
    # Placed in this file due to the circular import issue.
    """API configuration."""

    PROMPT_API: str = "https://internal.api.ml.stage.onclusive.com"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "sk-xx"
    CLAUDE_IPTC_ALIAS: str = "ml-iptc-topic-prediction"

    IPTC_RESPONSE_SCHEMA: Dict[str, str] = {
        "iptc category": "Answer the IPTC category",
    }
    DEFAULT_MODEL: str = "gpt-4o-mini"


settings = PromptBackendAPISettings()


def get_candidate_list(row, level):
    """Get a candidate topic of a given node."""
    if level == 1:
        node_name = "root"
        candidate_list = list(
            CANDIDATE_DICT_FIRST.get(node_name, {"dummy": "dummy"}).values()
        )
    elif level == 2:
        node_name = row["topic_1"]
        node_name = NAME_MAPPING_DICT_FIRST.get(node_name, node_name)
        candidate_list = list(
            CANDIDATE_DICT_SECOND.get(node_name, {"dummy": "dummy"}).values()
        )
    elif level == 3:
        node_name = row["topic_2"]
        node_name = NAME_MAPPING_DICT_SECOND.get(node_name, node_name)
        candidate_list = list(
            CANDIDATE_DICT_THIRD.get(node_name, {"dummy": "dummy"}).values()
        )
    elif level == 4:
        node_name = row["topic_3"]
        node_name = NAME_MAPPING_DICT_THIRD.get(node_name, node_name)
        candidate_list = list(
            CANDIDATE_DICT_FOURTH.get(node_name, {"dummy": "dummy"}).values()
        )

    return candidate_list


def get_col_name(level):
    """Get a column name of each level."""
    col_name = f"topic_{level}_llm"
    return col_name


async def generate_label_llm(row, session, level):
    """Invoke LLM to generate IPTC asynchronously."""
    candidate_list = get_candidate_list(row, level)

    # Construct the prompt string
    prompt = (
        "You are a topic analysis expert.\n"
        "You will be provided an article, delimited by < and >, and its title, delimited by $ and $. And a list of candidate categories, delimited by * and *.\n"
        "You need to classify the article into the most proper category, based on the article content and its title.\n\n"
        "You must do the analysis following the steps below:\n"
        "1. Read the article and its title to understand the main idea.\n"
        "2. Go through all the candidate categories which include the category name and its description, and think about the difference between the candidate categories.\n"
        "3. Classify the article into the most proper category.\n\n"
        "Output Constraint:\n"
        "Provide the output as a JSON object with the key 'iptc_category' and the value as the most proper category from the list of candidates.\n\n"
        "<article>{article}</article>\n"
        "<Title>{title}</Title>\n"
        "<Candidates>{candidates}</Candidates>"
    ).format(article=row["content"], title=row["title"], candidates=candidate_list)

    headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

    try:
        # Construct the URL with the endpoint and prompt
        url = "{}/api/v2/models/{}/generate?prompt={}".format(
            settings.PROMPT_API,
            settings.DEFAULT_MODEL,
            aiohttp.helpers.quote(prompt),  # Encode the prompt to be URL-safe
        )
        async with session.post(url, headers=headers, json={}) as response:
            try:
                output_content = await response.json()
            except aiohttp.ContentTypeError:
                response_text = await response.text()
                print(f"Failed to parse response as JSON. Response: {response_text}")
                return None

            if "generated" in output_content:
                try:
                    # Strip the '```json' and '```' markers if present and parse the 'generated' field as JSON
                    generated_text = (
                        output_content["generated"]
                        .strip("```json")
                        .strip("```")
                        .strip()
                    )
                    generated_content = json.loads(generated_text)

                    # Check if the parsed 'generated' JSON contains 'iptc_category'
                    if "iptc_category" in generated_content:
                        return generated_content["iptc_category"]
                    else:
                        print(
                            f"'iptc_category' not found in the generated content: {generated_content}"
                        )
                        return None
                except json.JSONDecodeError:
                    print(
                        f"Failed to parse 'generated' content as JSON: {output_content['generated']}"
                    )
                    return None
            else:
                print(f"'generated' key not found in the response: {output_content}")
                return None

    except Exception as e:
        # General exception handling for any other errors
        print(f"An unexpected error occurred. {e}")
        return None


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


def iptc_third_level_on_demand_feature_view(features_df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function to run the async enrichment."""
    level = 3
    features_df_with_label = asyncio.run(enrich_dataframe(features_df, level))

    df = pd.DataFrame()
    col_name = get_col_name(level)
    df[col_name] = features_df_with_label[col_name].astype(pd.StringDtype())
    return df


def iptc_fourth_level_on_demand_feature_view(features_df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function to run the async enrichment."""
    level = 4
    features_df_with_label = asyncio.run(enrich_dataframe(features_df, level))

    df = pd.DataFrame()
    col_name = get_col_name(level)
    df[col_name] = features_df_with_label[col_name].astype(pd.StringDtype())
    return df
