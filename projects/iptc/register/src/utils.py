
# Standard Library
import json
# from src.settings import PromptBackendAPISettings
from typing import Dict

# 3rd party libraries
import pandas as pd
import requests


class PromptBackendAPISettings:  # OnclusiveBaseSettings is not serializable
    """API configuration."""

    PROMPT_API: str = "http://prompt-backend:4000"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "1234"
    CLAUDE_IPTC_ALIAS: str = "ml-iptc-topic-prediction"

    IPTC_RESPONSE_SCHEMA: Dict[str, str] = {
        "iptc category": "Answer the IPTC category",
        "reason": "The reason for why you think it is this category",  # noqa: E501
    }
    DEFAULT_MODEL: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"


settings = PromptBackendAPISettings()


def generate_label_llm(title, article, candidates):
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


def iptc_llm_feature_view_2(features_df: pd.DataFrame) -> pd.DataFrame:
    candidates = [
        {
            "name": "arts, culture, entertainment and media",
            "description": "All forms of arts, entertainment, cultural heritage and media",
        },
        {
            "name": "conflict, war and peace",
            "description": "Acts of socially or politically motivated protest or violence, military activities, geopolitical conflicts, as well as resolution efforts",
        },
        {
            "name": "crime, law and justice",
            "description": "The establishment and/or statement of the rules of behaviour in society, the enforcement of these rules, breaches of the rules, the punishment of offenders and the organisations and bodies involved in these activities",
        },
        {
            "name": "disaster, accident and emergency incident",
            "description": "Man made or natural event resulting in loss of life or injury to living creatures and/or damage to inanimate objects or property",
        },
        {
            "name": "economy, business and finance",
            "description": "All matters concerning the planning, production and exchange of wealth.",
        },
        {
            "name": "education",
            "description": "All aspects of furthering knowledge, formally or informally",
        },
        {
            "name": "environment",
            "description": "All aspects of protection, damage, and condition of the ecosystem of the planet earth and its surroundings.",
        },
        {
            "name": "health",
            "description": "All aspects of physical and mental well-being",
        },
        {
            "name": "human interest",
            "description": "Item that discusses individuals, groups, animals, plants or other objects in an emotional way",
        },
        {
            "name": "labour",
            "description": "Social aspects, organisations, rules and conditions affecting the employment of human effort for the generation of wealth or provision of services and the economic support of the unemployed.",
        },
        {
            "name": "lifestyle and leisure",
            "description": "Activities undertaken for pleasure, relaxation or recreation outside paid employment, including eating and travel.",
        },
        {
            "name": "politics",
            "description": "Local, regional, national and international exercise of power, or struggle for power, and the relationships between governing bodies and states.",
        },
        {
            "name": "religion",
            "description": "Belief systems, institutions and people who provide moral guidance to followers",
        },
        {
            "name": "science and technology",
            "description": "All aspects pertaining to human understanding of, as well as methodical study and research of natural, formal and social sciences, such as astronomy, linguistics or economics",
        },
        {
            "name": "society",
            "description": "The concerns, issues, affairs and institutions relevant to human social interactions, problems and welfare, such as poverty, human rights and family planning",
        },
        {
            "name": "sport",
            "description": "Competitive activity or skill that involves physical and/or mental effort and organisations and bodies involved in these activities",
        },
        {
            "name": "weather",
            "description": "The study, prediction and reporting of meteorological phenomena",
        },
    ]

    df = pd.DataFrame()
    topic_label = [
        generate_label_llm(title, content, candidates)
        # (title+content)
        for title, content in zip(
            features_df["title"].values, features_df["content"].values
        )
    ]
    df["topic_1_llm"] = pd.Series(topic_label).astype(pd.StringDtype())
    return df
