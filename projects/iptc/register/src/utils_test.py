import json
from class_dict import CANDIDATE_DICT_FIRST
import pandas as pd
import requests
from typing import Dict
import asyncio
import aiohttp

class PromptBackendAPISettings:  # OnclusiveBaseSettings is not serializable.
    # Placed in this file due to the circular import issue.
    """API configuration."""

    PROMPT_API: str = "https://internal.api.ml.prod.onclusive.com"#"http://prompt-backend:4000"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "sk-e7OtXaIMzp7wxjJkz7kILyO3gYrrh0ez"#"1234"
    CLAUDE_IPTC_ALIAS: str = "ml-iptc-topic-prediction"

    IPTC_RESPONSE_SCHEMA: Dict[str, str] = {
        "iptc category": "Answer the IPTC category",
    }
    DEFAULT_MODEL: str = "gpt-4o-mini"


settings = PromptBackendAPISettings()


def generate_label_llm(row):
    """Invoke LLM to generate IPTC ."""
    input_dict = {
        "input": {"title": row['title'], "article": row['content'], "candidates": CANDIDATE_DICT_FIRST},
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
    df["topic_1_llm"] = features_df.apply(generate_label_llm,axis=1).astype(pd.StringDtype())
    return df

async def generate_label_llm_2(row, session):
    """Invoke LLM to generate IPTC asynchronously."""
    input_dict = {
        "input": {"title": row['title'], "article": row['content'], "candidates": CANDIDATE_DICT_FIRST},
        "output": settings.IPTC_RESPONSE_SCHEMA,
    }
    headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

    async with session.post(
        "{}/api/v2/prompts/{}/generate/model/{}".format(
            settings.PROMPT_API, settings.CLAUDE_IPTC_ALIAS, settings.DEFAULT_MODEL
        ),
        headers=headers,
        json=input_dict
    ) as response:
        output_content = await response.json()
        return output_content["iptc category"]

async def enrich_dataframe(features_df: pd.DataFrame) -> pd.DataFrame:
    """On-demand feature view transformation with async."""
    
    async with aiohttp.ClientSession() as session:
        tasks = [generate_label_llm_2(row, session) for _, row in features_df.iterrows()]
        features_df['topic_1_llm'] = await asyncio.gather(*tasks)
    return features_df

def iptc_first_level_on_demand_feature_view_2(features_df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper function to run the async enrichment."""
    
    df = asyncio.run(enrich_dataframe(features_df))
    return df.astype({'topic_1_llm': pd.StringDtype()})