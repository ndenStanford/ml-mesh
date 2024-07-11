"""Topic handler."""
# isort: skip_file

# Standard Library
import re
from typing import List, Dict, Union, Optional, Tuple

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

    def topic_inference(
        self, articles: List[str], entity_list: Optional[str] = None
    ) -> Dict[str, str]:
        """LLM inference function for the articles.

        Args:
            articles(list): list of str
            entity_list(Optional[str]): string representing a list of entities in the query
        Output:
            topic summary & impact(dict): dict[str,str]
        """
        # transfer article to the format used in prompt
        processed_article = {
            f"Article {i}": article for i, article in enumerate(articles)
        }

        if entity_list:
            topic_alias_claude = settings.CLAUDE_TOPIC_WITH_ENTITY_ALIAS
            topic_alias_gpt = settings.GPT_TOPIC_WITH_ENTITY_ALIAS
            input_dict = {
                "input": {"articles": processed_article, "entity_list": entity_list},
                "output": settings.TOPIC_RESPONSE_SCHEMA,
            }
        else:
            topic_alias_claude = settings.CLAUDE_TOPIC_ALIAS
            topic_alias_gpt = settings.GPT_TOPIC_ALIAS
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

    def entity_query_extract(self, boolean_query: str) -> str:
        """Extract entity from boolean query.

        Args:
            boolean_query(str): boolean query
        Output:
            entity_list (str): entity list represented by string
        """
        entity_query_alias_claude = settings.CLAUDE_QUERY_ENTITY_EXTRACTION_ALIAS
        entity_query_alias_gpt = settings.GPT_QUERY_ENTITY_EXTRACTION_ALIAS

        input_dict = {
            "input": {
                "query": boolean_query,
            },
            "output": settings.ENTITY_RESPONSE_SCHEMA,
        }

        output_content = None
        try:
            q = self.call_api(
                entity_query_alias_claude, settings.HAIKU_CLAUDE_MODEL, input_dict
            )
            output_content = json.loads(q.content)
            if not isinstance(output_content, dict):
                raise ValueError("Claude topic response is not a valid string")
        except Exception as e:
            logging.error(f"Failed with Claude in Topic: {e}")

        if (not output_content) or not isinstance(output_content, dict):
            q = self.call_api(entity_query_alias_gpt, settings.GPT_MODEL, input_dict)
            output_content = json.loads(q.content)

        entity_list = output_content["entity_list"]
        return entity_list

    def summary_inference(
        self, articles: List[str], entity_list: Optional[str] = None
    ) -> Dict[str, str]:
        """LLM summary inference function for the articles.

        Args:
            articles(list): list of str
            entity_list(Optional[str]): string representing a list of entities in the query
        Output:
            summary & theme(dict): dict[str,str]
        """
        # transfer article to the format used in prompt
        processed_article = {
            f"Article {i}": article for i, article in enumerate(articles)
        }

        if entity_list:
            summary_alias_claude = settings.CLAUDE_SUMMARY_WITH_ENTITY_ALIAS
            summary_alias_gpt = settings.GPT_SUMMARY_WITH_ENTITY_ALIAS
            input_dict = {
                "input": {"articles": processed_article, "entity_list": entity_list},
                "output": settings.SUMMARY_RESPONSE_SCHEMA,
            }
        else:
            summary_alias_claude = settings.CLAUDE_SUMMARY_ALIAS
            summary_alias_gpt = settings.GPT_SUMMARY_ALIAS
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

    def summary_quality(self, summary: str, entities: str) -> str:
        """Return whether quality of summary is good or bad.

        Args:
            summary(str): high level topic summary
            entities(str): entity list represented by string
        Output:
            bool (str): quality of summary is good or bad
        """
        input_dict = {
            "input": {"summary": summary, "entities": entities},
            "output": settings.SUMMARY_QUALITY_RESPONSE_SCHEMA,
        }

        q = self.call_api(
            settings.CLAUDE_SUMMARY_QUALITY_ALIAS, settings.DEFAULT_MODEL, input_dict
        )
        output_content = json.loads(q.content)
        not_different_themes = (
            output_content.get("different_themes", "").lower() == "no"
        )
        entities_related = output_content.get("entities_related", "").lower() == "yes"

        if entities == "[]":
            return not_different_themes
        else:
            return not_different_themes and entities_related

    def aggregate(
        self, article: List[str], boolean_query: Optional[str] = None
    ) -> Tuple[
        Dict[str, Union[Dict[str, Union[str, ImpactCategoryLabel]], str, None]],
        Union[str, None],
    ]:
        """Aggregate topic & summary results together.

        Args:
            article(list): list of str
            boolean_query(Optional[str]): boolean query
        Output:
            merged_result (dict): dict
        """
        article = self.pre_process(article)

        if boolean_query is not None:
            entity_list = self.entity_query_extract(boolean_query)
        else:
            entity_list = None

        topic_result = self.topic_inference(article, entity_list)
        topic_final_result = self.post_process(topic_result)
        summary_result = self.summary_inference(article, entity_list)
        topic_summary_quality = self.summary_quality(
            summary_result["summary"], entity_list or "[]"
        )

        merged_result: Dict[
            str, Union[Dict[str, Union[str, ImpactCategoryLabel]], str, None]
        ] = {}
        merged_result.update(topic_final_result)
        merged_result.update(summary_result)
        return (merged_result, topic_summary_quality)
