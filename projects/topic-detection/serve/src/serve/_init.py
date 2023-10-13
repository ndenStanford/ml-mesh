"""Service initialization."""

# Standard Library
from typing import Optional

# 3rd party libraries
import requests
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.core.logging import get_default_logger


# from src.settings import settings


logger = get_default_logger(__name__)


class Settings(BaseSettings):
    """API configuration."""

    API_NAME: str = "Topic detection"
    # API description
    API_DESCRIPTION: str = ""
    # API environment
    ENVIRONMENT: str = "dev"
    # Betterstack heartbeat key
    BETTERSTACK_KEY: str = ""
    # Debug level
    DEBUG: bool = True
    # API runtime
    KUBERNETES_IN_POD: bool = False
    # Logging level
    LOGGING_LEVEL: str = "info"
    # documentation endpoint
    DOCS_URL: Optional[str] = "/topic-detection/docs"
    OPENAPI_URL: Optional[str] = "/topic-detection/openapi.json"
    # OpenAI api key
    OPENAI_API_KEY: str = ""
    # Prompt url
    PROMPT_API: str = "http://prompt-backend:4000"
    # PROMPT_API: str = "http://0.0.0.0:4000"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "1234"
    # interested aspects/categories
    CATEGORY_LIST = [
        "Opportunities",
        "Risk detection",
        "Threats for the brand",
        "Company or spokespersons",
        "Brand Reputation",
        "CEO Reputation",
        "Customer Response",
        "Stock Price Impact",
        "Industry trends",
    ]
    # prompt for iteratively input; each time one category only
    PROMPT_DICT = {
        "analysis": {
            "alias": "topic-detection-analysis",
            "template": """
                I want you to summarize the protential impact on the given category in the target industry, based on all the articles together.

                I will give you a target industry delimited by *, the target category delimited by < and >,
                and many articles related to this industry delimited by triple backticks.

                Target industry: *{target_industry}*

                Target category: <{target_category}>

                For the category isn't not related to the articles, output 'Not mentioned'.

                Generate your output in following format:
                For category Risk detection, the articles suggest that the risk detection in the science and technology industry is
                related to the dependency on imported components, especially semiconductor ones, volatility in weather patterns,
                and the limited understanding about the universe including black holes.

                {content}
                """,  # noqa: E501
        },
        "aggregate": {
            "alias": "topic-analysis-aggregation",
            "template": """
                I want you to provide a concise summary that combines the main points of the following summaries.

                Those summaries are from multiple articles, focusing on a given aspect of a target industry.

                I will give you the target industry delimited by *, a target category delimited by < and >,
                and many summaries from articles related to this industry delimited by triple backticks.

                Target industry: *{target_industry}*

                Target category: <{target_category}>

                Restrict your output in 100 words.

                {Summary}
        """,  # noqa: E501
        },
    }


settings = Settings()


def init() -> None:
    """App initialization."""
    logger.info("Setting up prompts...")
    _setup_prompts()


def _setup_prompts() -> None:
    """Setup prompts."""
    headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

    for prompt_key in settings.PROMPT_DICT.keys():
        # print('prompt_dict :',prompt_dict)
        alias = settings.PROMPT_DICT[prompt_key]["alias"]
        template = settings.PROMPT_DICT[prompt_key]["template"]
        requests.post(
            f"{settings.PROMPT_API}/api/v1/prompts?template={template}&alias={alias}",  # noqa: E501
            headers=headers,
        )
    return
