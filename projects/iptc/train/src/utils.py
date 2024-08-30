"""Utility functions."""

# Standard Library
import asyncio
import json
import logging
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

# 3rd party libraries
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Source
from src.class_dict import (
    CANDIDATE_DICT_FIRST,
    CANDIDATE_DICT_SECOND,
    CANDIDATE_DICT_THIRD,
    CLASS_DICT_FIRST,
    CLASS_DICT_SECOND,
    CLASS_DICT_THIRD,
)


logging.basicConfig(level=logging.INFO)


def compute_metrics(pred):  # type: ignore[no-untyped-def]
    """Compute metrics function for binary classification."""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="weighted"
    )
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}


def find_num_labels(  # type: ignore[no-untyped-def]
    level, first_level_root=None, second_level_root=None
):
    """Retrieve the number of labels from the CLASS_DICT file."""
    if level == 1:
        return len(CLASS_DICT_FIRST["root"])
    elif level == 2:
        return len(CLASS_DICT_SECOND[first_level_root])
    elif level == 3:
        return len(CLASS_DICT_THIRD[second_level_root])


def extract_model_id(project: str) -> str:
    """Extracts the model ID from a project string.

    Args:
        project (str): The project string, e.g., 'onclusive/iptc-00000000'.

    Returns:
        str: The extracted model ID.

    Raises:
        ValueError: If the model ID cannot be found in the project string.
    """
    match = re.search(r"onclusive/iptc-(.+)", project)
    if match:
        return match.group(1)  # Return the matched group, which is the model ID
    else:
        raise ValueError(f"Model ID not found in project string: '{project}'")


def find_category_for_subcategory(  # type: ignore[no-untyped-def]
    class_dict, target_subcategory
):
    """Function to find the top-level category for a given sub-category."""
    for top_category, subcategories in class_dict.items():
        if target_subcategory in subcategories.values():
            return top_category


def topic_conversion(df):  # type: ignore[no-untyped-def]
    """Update the topic name to fix the discrepencies between class_dict and training data."""
    df["topic_1"] = df["topic_1"].replace(
        ["arts, culture and entertainment"], "arts, culture, entertainment and media"
    )
    df["topic_1"] = df["topic_1"].replace(
        ["conflicts, war and peace"], "conflict, war and peace"
    )
    if "topic_2" in df.columns:
        df["topic_2"] = df["topic_2"].replace(
            ["religious facilities"], "religious facility"
        )
    if "topic_3" in df.columns:
        df["topic_3"] = df["topic_3"].replace(["bullfighting "], "bullfighting")
    return df


class PromptBackendAPISettings:
    """API configuration."""

    PROMPT_API: str = "https://internal.api.ml.prod.onclusive.com"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "sk-xx"
    CLAUDE_IPTC_ALIAS: str = "ml-iptc-topic-prediction"

    IPTC_RESPONSE_SCHEMA: Dict[str, str] = {
        "iptc category": "Answer the IPTC category",
    }
    DEFAULT_MODEL: str = "gpt-4o-mini"


settings = PromptBackendAPISettings()


def get_candidate_list(row, level):
    """Get candidate description."""
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
    elif level == 3:
        node_name = row["topic_2"]
        candidate_list = list(
            CANDIDATE_DICT_THIRD.get(node_name, {"dummy": "dummy"}).values()
        )

    return candidate_list


def get_col_name(level):
    """Get column name."""
    col_name = f"topic_{level}_llm"
    return col_name


def fetch_label_llm(url: str, headers: Dict[str, str], data: Dict) -> Dict:
    """Synchronous function to make the API request."""
    try:
        # Ensure the data is a properly formatted JSON dictionary
        logging.info(
            f"Data being sent: {json.dumps(data, ensure_ascii=False, indent=2)}"
        )

        headers.update(
            {"Content-Type": "application/json"}
        )  # Ensure the correct content type is set

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),  # JSON encode the dictionary
            headers=headers,
            method="POST",
        )

        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as e:
        logging.error(f"HTTP error: {e.code} - {e.reason}")
        logging.error(f"Response: {e.read().decode('utf-8')}")
        raise


async def generate_label_llm(row, level):
    """Invoke LLM to generate IPTC asynchronously using the standard library."""
    candidate_list = get_candidate_list(row, level)
    input_dict = {
        "input": {
            "title": row.get("title", ""),
            "article": row.get("content", ""),
            "candidates": candidate_list,
        },
        "output": settings.IPTC_RESPONSE_SCHEMA,
    }
    headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}
    url = "{}/api/v2/prompts/{}/generate/model/{}".format(
        settings.PROMPT_API, settings.CLAUDE_IPTC_ALIAS, settings.DEFAULT_MODEL
    )

    logging.info(f"Sending request to {url} with payload: {input_dict}")

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        output_content = await loop.run_in_executor(
            pool, fetch_label_llm, url, headers, input_dict
        )

    return output_content["iptc category"]


async def enrich_dataframe(features_df: pd.DataFrame, level) -> pd.DataFrame:
    """On-demand feature view transformation with async using the standard library."""
    # Make a copy of the DataFrame to avoid modifying the original
    features_df_copy = features_df.copy()
    col_name = get_col_name(level)
    tasks = [generate_label_llm(row, level) for _, row in features_df_copy.iterrows()]
    features_df_copy[col_name] = await asyncio.gather(*tasks)
    return features_df_copy


def iptc_first_level_on_demand_feature_view(features_df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function to run the async enrichment."""
    features_df_with_label = asyncio.run(enrich_dataframe(features_df, 1))

    df = pd.DataFrame()
    df["topic_1_llm"] = features_df_with_label["topic_1_llm"].astype(pd.StringDtype())
    return df


def iptc_second_level_on_demand_feature_view(features_df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function to run the async enrichment."""
    features_df_with_label = asyncio.run(enrich_dataframe(features_df, 2))

    df = pd.DataFrame()
    df["topic_2_llm"] = features_df_with_label["topic_2_llm"].astype(pd.StringDtype())
    return df


def iptc_third_level_on_demand_feature_view(features_df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function to run the async enrichment."""
    features_df_with_label = asyncio.run(enrich_dataframe(features_df, 3))

    df = pd.DataFrame()
    df["topic_3_llm"] = features_df_with_label["topic_3_llm"].astype(pd.StringDtype())
    return df
