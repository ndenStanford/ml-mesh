"""Utility functions."""

# Standard Library
import asyncio
import re
from typing import Dict

# 3rd party libraries
import aiohttp
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Source
from src.class_dict import CLASS_DICT_FIRST, CLASS_DICT_SECOND, CLASS_DICT_THIRD


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


class PromptBackendAPISettings:  # OnclusiveBaseSettings is not serializable.
    # Placed in this file due to the circular import issue.
    """API configuration."""

    PROMPT_API: str = "https://internal.api.ml.prod.onclusive.com"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "sk-e7OtXaIMzp7wxjJkz7kILyO3gYrrh0ez"
    CLAUDE_IPTC_ALIAS: str = "ml-iptc-topic-prediction"

    IPTC_RESPONSE_SCHEMA: Dict[str, str] = {
        "iptc category": "Answer the IPTC category",
    }
    DEFAULT_MODEL: str = "gpt-4o-mini"


settings = PromptBackendAPISettings()


async def generate_label_llm(row, session):
    """Invoke LLM to generate IPTC asynchronously."""
    input_dict = {
        "input": {
            "title": row["title"],
            "article": row["content"],
            "candidates": CLASS_DICT_FIRST,
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


async def enrich_dataframe(features_df: pd.DataFrame) -> pd.DataFrame:
    """On-demand feature view transformation with async."""
    # Make a copy of the DataFrame to avoid modifying the original
    features_df_copy = features_df.copy()

    async with aiohttp.ClientSession() as session:
        tasks = [
            generate_label_llm(row, session) for _, row in features_df_copy.iterrows()
        ]
        features_df_copy["topic_1_llm"] = await asyncio.gather(*tasks)
    return features_df_copy


def iptc_first_level_on_demand_feature_view(features_df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function to run the async enrichment."""
    features_df_with_label = asyncio.run(enrich_dataframe(features_df))

    df = pd.DataFrame()
    df["topic_1_llm"] = features_df_with_label["topic_1_llm"].astype(pd.StringDtype())
    return df
