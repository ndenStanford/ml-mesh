"""Topic handler."""
# isort: skip_file

# Standard Library
import re
from typing import List, Dict, Union

# 3rd party libraries
import requests
import json

# from multiprocessing import Pool, cpu_count

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.preprocess import remove_html, remove_whitespace

# Source
from src.settings import get_api_settings, get_settings  # type: ignore[attr-defined]

logger = get_default_logger(__name__)
settings = get_api_settings()
model_settings = get_settings()


class TopicHandler:
    """Topic summarization with prompt backend."""

    def inference(self, articles: List[str]) -> Dict[str, str]:
        """LLM inference function for the articles.

        Args:
            articles(list): list of str
        Output:
            topic summary & impact(dict): dict[str,str]
        """
        claude_alias = settings.PROMPT_ALIAS["claude_topic"]
        # gpt_alias = settings.PROMPT_ALIAS["gpt_topic"]
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
                settings.PROMPT_API, claude_alias, settings.DEFAULT_MODEL
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
        # grouped_article = self.group(article)
        # topic_result = self.topic_aggregate(grouped_article)
        # summary_result = self.summary_aggregate(grouped_article)
        topic_result = self.inference(article)
        merged_result: Dict[str, Union[Dict[str, str], str, None]] = {}
        merged_result.update(topic_result)
        # merged_result.update(summary_result)
        return merged_result
