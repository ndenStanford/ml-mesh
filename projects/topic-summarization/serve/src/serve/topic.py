"""Topic handler."""
# isort: skip_file

# Standard Library
import re
from typing import List, Dict, Union

# 3rd party libraries
import requests
import json
import logging

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.preprocess import remove_html, remove_whitespace
from onclusiveml.serving.serialization.topic_summarization.v1 import ImpactCategoryLabel

# Source
from src.settings import get_api_settings, get_settings  # type: ignore[attr-defined]

logger = get_default_logger(__name__)
settings = get_api_settings()
model_settings = get_settings()
impact_category = model_settings.IMPACT_CATEGORIES


class TopicHandler:
    """Topic summarization with prompt backend."""

    impact_map: Dict[str, ImpactCategoryLabel] = {
        "low": ImpactCategoryLabel.LOW,
        "medium": ImpactCategoryLabel.MID,
        "high": ImpactCategoryLabel.HIGH,
    }

    def call_api(
        self, prompt_alias: str, model_name: str, input_dict: Dict
    ) -> requests.Response:
        """Call prompt backend api.

        Args:
            prompt_alias(str): the prompt
            model_name(str): gpt or claude
            input_dict(Dict): processed articles
        Output:
            summary & impact(dict): dict[str,str]
        """
        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}
        q = requests.post(
            "{}/api/v2/prompts/{}/generate/model/{}".format(
                settings.PROMPT_API, prompt_alias, model_name
            ),
            headers=headers,
            json=input_dict,
        )
        return q

    def topic_inference(self, articles: List[str]) -> Dict[str, str]:
        """LLM inference function for the articles.

        Args:
            articles(list): list of str
        Output:
            topic summary & impact(dict): dict[str,str]
        """
        topic_alias_claude = settings.CLAUDE_TOPIC_ALIAS
        topic_alias_gpt = settings.GPT_TOPIC_ALIAS
        # transfer article to the format used in prompt
        processed_article = {
            f"Article {i}": article for i, article in enumerate(articles)
        }

        input_dict = {
            "input": {
                "articles": processed_article,
            },
            "output": settings.TOPIC_RESPONSE_SCHEMA,
        }

        output_content = None
        try:
            q = self.call_api(topic_alias_claude, settings.DEFAULT_MODEL, input_dict)
            output_content = json.loads(q.content)
            if not isinstance(output_content, dict):
                raise ValueError("Claude topic response is not a valid dict")
        except Exception as e:
            logging.error(f"Failed with Sonnet in Topic: {e}")

        if (not output_content) or not isinstance(output_content, dict):
            q = self.call_api(topic_alias_gpt, settings.GPT_MODEL, input_dict)
            output_content = json.loads(q.content)

        return output_content

    def summary_inference(self, articles: List[str]) -> Dict[str, str]:
        """LLM summary inference function for the articles.

        Args:
            articles(list): list of str
        Output:
            summary & theme(dict): dict[str,str]
        """
        summary_alias_claude = settings.CLAUDE_SUMMARY_ALIAS
        summary_alias_gpt = settings.GPT_SUMMARY_ALIAS
        # transfer article to the format used in prompt
        processed_article = {
            f"Article {i}": article for i, article in enumerate(articles)
        }

        input_dict = {
            "input": {
                "articles": processed_article,
            },
            "output": settings.SUMMARY_RESPONSE_SCHEMA,
        }

        output_content = None
        try:
            q = self.call_api(summary_alias_claude, settings.DEFAULT_MODEL, input_dict)
            output_content = json.loads(q.content)
            if not isinstance(output_content, dict):
                raise ValueError("Claude summary response is not a valid dict")
        except Exception as e:
            logging.error(f"Failed with Sonnet in Summary: {e}")

        if (not output_content) or not isinstance(output_content, dict):
            q = self.call_api(summary_alias_gpt, settings.GPT_MODEL, input_dict)
            output_content = json.loads(q.content)

        return output_content

    def pre_process(self, article: List[str]) -> List[str]:
        """Pre process function for articles.

        Args:
            article(list): list of str
        Output:
            processed_article(list): list of str
        """
        article = [re.sub("\n+", " ", text) for text in article]
        processed_article = [remove_whitespace(remove_html(text)) for text in article]
        return processed_article

    def post_process(
        self, topic_result: Dict[str, str]
    ) -> Dict[str, Dict[str, Union[str, ImpactCategoryLabel]]]:
        """Transfer the topic inference output to multi-layer json."""
        final_topic: Dict[str, Dict[str, Union[str, ImpactCategoryLabel]]] = {}
        for key, value in topic_result.items():
            if "_" in key:
                prefix, suffix = key.split("_")
                category = prefix
                if category not in final_topic:
                    final_topic[category] = {}
                final_topic[category][suffix] = value
            else:
                category = key
                if category not in final_topic and value != "N/A":
                    final_topic[category] = {"summary": value}
        for key in final_topic:
            impact_value = final_topic[key]["impact"].lower()
            final_topic[key]["impact"] = self.impact_map[impact_value]

        return final_topic

    def aggregate(
        self, article: List[str]
    ) -> Dict[str, Union[Dict[str, Union[str, ImpactCategoryLabel]], str, None]]:
        """Aggregate topic & summary results together.

        Args:
            article(list): list of str
        Output:
            merged_result (dict): dict
        """
        article = self.pre_process(article)
        topic_result = self.topic_inference(article)
        topic_final_result = self.post_process(topic_result)
        summary_result = self.summary_inference(article)
        merged_result: Dict[
            str, Union[Dict[str, Union[str, ImpactCategoryLabel]], str, None]
        ] = {}
        merged_result.update(topic_final_result)
        merged_result.update(summary_result)
        return merged_result
