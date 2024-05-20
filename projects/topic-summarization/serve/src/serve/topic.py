"""Topic handler."""
# isort: skip_file

# Standard Library
import re
from typing import List, Dict, Union

# 3rd party libraries
import requests
import json

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.preprocess import remove_html, remove_whitespace

# Source
from src.settings import get_api_settings, get_settings  # type: ignore[attr-defined]

logger = get_default_logger(__name__)
settings = get_api_settings()
model_settings = get_settings()
impact_category = model_settings.IMPACT_CATEGORIES


class TopicHandler:
    """Topic summarization with prompt backend."""

    def topic_inference(self, articles: List[str]) -> Dict[str, str]:
        """LLM inference function for the articles.

        Args:
            articles(list): list of str
        Output:
            topic summary & impact(dict): dict[str,str]
        """
        topic_alias = settings.TOPIC_ALIAS
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

        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/api/v2/prompts/{}/generate/model/{}".format(
                settings.PROMPT_API, topic_alias, settings.DEFAULT_MODEL
            ),
            headers=headers,
            json=input_dict,
        )

        output_content = json.loads(q.content)

        return output_content

    def summary_inference(self, articles: List[str]) -> Dict[str, str]:
        """LLM summary inference function for the articles.

        Args:
            articles(list): list of str
        Output:
            summary & theme(dict): dict[str,str]
        """
        summary_alias = settings.SUMMARY_ALIAS
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

        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/api/v2/prompts/{}/generate/model/{}".format(
                settings.PROMPT_API, summary_alias, settings.DEFAULT_MODEL
            ),
            headers=headers,
            json=input_dict,
        )

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

    def post_process(self, topic_result: Dict[str, str]) -> Dict[str, Dict[str, str]]:
        """Transfer the topic inference output to multi-layer json."""
        final_topic: Dict[str, Dict[str, str]] = {}
        for key, value in topic_result.items():
            if "_" in key:
                prefix, suffix = key.split("_")
                category = impact_category[prefix]
                if category not in final_topic:
                    final_topic[category] = {}
                final_topic[category][suffix] = value
            else:
                category = key
                if category not in final_topic and value != "N/A":
                    final_topic[category] = {"summary": value}
        return final_topic

    def aggregate(
        self, article: List[str]
    ) -> Dict[str, Union[Dict[str, str], str, None]]:
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
        merged_result: Dict[str, Union[Dict[str, str], str, None]] = {}
        merged_result.update(topic_final_result)
        merged_result.update(summary_result)
        return merged_result
