"""Topic handler."""
# isort: skip_file

# Standard Library
import re
from typing import List

# 3rd party libraries
import requests
import json

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.preprocess import remove_html, remove_whitespace

# Source
from src.serve._init import Settings

logger = get_default_logger(__name__)
# setting class
settings = Settings()


class TopicHandler:
    """Detect trends by GPT."""

    # use gpt to generate summary on certain category; will be called in aggregate.
    def inference(
        self,
        article: List[str],
        category: str,
    ) -> str:
        """Topic detection handler method.

        Args:
            article (list): list of str
            category (str): target category, one of ['Risk detection', 'Opportunities',
            'Threats for the brand','Company or spokespersons', 'Brand Reputation',
            'CEO Reputation', 'Customer Response', 'Stock Price Impact',
            'Industry trends']
        """
        alias = "ml-topic-summarization-single-analysis"
        # transfer article to the format used in prompt
        processed_article = ""
        for i in range(len(article)):
            text = article[i]
            processed_article += (
                "\n    Article " + str(i) + ": '''" + text + "''' " + "\n"
            )

        input_dict = {
            "target_category": category,
            "content": processed_article,
        }  # input target category & articles
        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/api/v1/prompts/{}/generate".format(settings.PROMPT_API, alias),
            headers=headers,
            json=input_dict,
        )

        output_content = json.loads(json.loads(q.content)["generated"])

        key = category if category in output_content else f"<{category}>"
        return output_content.get(key)

    # use gpt to generate summary for multiple articles together; will be called in aggregate.
    def summary(
        self,
        article: List[str],
    ) -> str:
        """Summarize multiple articles at same time.

        Args:
            article (list): list of str
        """
        alias = "ml-multi-articles-summarization"
        # transfer article to the format used in prompt
        processed_article = ""
        for i in range(len(article)):
            text = article[i]
            processed_article += (
                "\n    Article " + str(i) + ": '''" + text + "''' " + "\n"
            )

        input_dict = {
            "content": processed_article,
        }  # input articles
        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/api/v1/prompts/{}/generate".format(settings.PROMPT_API, alias),
            headers=headers,
            json=input_dict,
        )
        return json.loads(json.loads(q.content)["generated"])["Summary"]

    def summary_aggregate(self, article: list) -> dict:
        """Function for aggregating summary and generating theme."""
        num_article = len(article)
        n = 10  # group size
        record = {"Summary": None, "Theme": None}
        # do topic analysis for each category
        art_index = 0
        record_cate = []
        # divide the articles into groups and summarize each group
        while art_index < num_article:
            end_index = min(art_index + n, num_article)
            input_article = article[art_index:end_index]  # E203
            res_now = self.summary(input_article)
            record_cate.append(res_now)
            art_index += n

        processed_summary = "\n".join(
            [
                f"Summary {index + 1}: '''{article}'''"
                for index, article in enumerate(record_cate)
            ]
        )

        alias = "ml-articles-summary-aggregation"
        input_dict = {"Summary": processed_summary}  # input target category & articles
        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/api/v1/prompts/{}/generate".format(settings.PROMPT_API, alias),
            headers=headers,
            json=input_dict,
        )

        output_content = json.loads(json.loads(q.content)["generated"])
        record["Summary"] = output_content["Summary"]
        record["Theme"] = output_content["Theme"]

        return record

    def topic_aggregate(self, article: list) -> dict:
        """Function for aggregating topic analysis results together."""
        num_article = len(article)
        n = 10  # group size
        category_list = settings.CATEGORY_LIST
        record = {cate: None for cate in category_list}
        # do topic analysis for each category
        for category in category_list:
            art_index = 0
            record_cate = []
            # divide the articles into groups and summarize each group
            while art_index < num_article:
                end_index = min(art_index + n, num_article)
                input_article = article[art_index:end_index]  # E203
                res_now = self.inference(input_article, category)
                record_cate.append(res_now)
                art_index += n

            processed_summary = "\n".join(
                [
                    f"Summary {index + 1}: '''{article}'''"
                    for index, article in enumerate(record_cate)
                ]
            )

            alias = "ml-topic-summarization-aggregate"

            input_dict = {
                "target_category": category,
                "Summary": processed_summary,
            }  # input target category & articles
            headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

            q = requests.post(
                "{}/api/v1/prompts/{}/generate".format(settings.PROMPT_API, alias),
                headers=headers,
                json=input_dict,
            )

            output_content = json.loads(json.loads(q.content)["generated"])
            record[category] = output_content[category]

        return record

    def pre_process(self, article: list) -> list:
        """Pre process function for articles."""
        article = [re.sub("\n+", " ", text) for text in article]
        processed_article = [remove_whitespace(remove_html(text)) for text in article]
        return processed_article

    def aggregate(self, article: list) -> dict:
        """Aggregate topic & summary results together."""
        article = self.pre_process(article)
        topic_result = self.topic_aggregate(article)
        summary_result = self.summary_aggregate(article)
        merged_result = {**topic_result, **summary_result}
        return merged_result
