"""Topic handler."""
# isort: skip_file

# Standard Library
import datetime
import re
from typing import Any, Dict, List

# 3rd party libraries
import requests
import json

# Internal libraries
# Internal library
from onclusiveml.core.logging import get_default_logger

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

    def aggregate(self, article: list) -> dict:
        """Function for aggregating results together, both topic analysis and summarization."""
        num_article = len(article)
        n = 10  # group size
        category_list = settings.CATEGORY_LIST
        record = {cate: None for cate in category_list + ["Summary"]}
        # do topic analysis for each category
        for category in category_list + ["Summary"]:
            # print('current category : ', cate)
            art_index = 0
            record_cate = []
            # divide the articles into groups and summarize each group
            while art_index < num_article:
                end_index = min(art_index + n, num_article)
                input_article = article[art_index:end_index]  # E203
                res_now = (
                    self.inference(input_article, category)
                    if category != "Summary"
                    else self.summary(input_article)
                )
                record_cate.append(res_now)
                art_index += n

            processed_summary = "\n".join(
                [
                    f"Summary {index + 1}: '''{article}'''"
                    for index, article in enumerate(record_cate)
                ]
            )

            alias = (
                "ml-topic-summarization-aggregate"
                if category != "Summary"
                else "ml-articles-summary-aggregation"
            )

            input_dict = (
                {
                    "target_category": category,
                    "Summary": processed_summary,
                }
                if category != "Summary"
                else {"Summary": processed_summary}
            )  # input target category & articles
            headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

            q = requests.post(
                "{}/api/v1/prompts/{}/generate".format(settings.PROMPT_API, alias),
                headers=headers,
                json=input_dict,
            )

            output_content = json.loads(json.loads(q.content)["generated"])
            record[category] = output_content[category]
            if category == "Summary":
                record["Theme"] = output_content["Theme"]

        return record

    def pre_process(self, article: list) -> list:
        """Pre process function for articles."""
        article = [re.sub("\n+", " ", text) for text in article]
        return article

    def postprocess(self, article: dict) -> dict:
        """Post process function for generated outputs."""
        for k in article.keys():
            article[k] = re.sub("\n+", " ", article[k])
        return article


_service = TopicHandler()


def handle(data: Any) -> Dict[str, dict]:
    """The handler."""
    try:
        if data is None:
            return {}

        if "body" not in data[0]:
            logger.warning(
                "Malformed request, content does not contain a body key."
                "Is your request properly formatted as json?"
            )
            return {}

        data = data[0]["body"]

        if type(data) == bytearray:
            data = eval(data)

        content = data["content"]

        if content is None or content == "":
            logger.warning(
                "Content field is empty. This will result in no summary being returned"
            )

        article = _service.pre_process(content)

        starttime = datetime.datetime.utcnow()
        topic = _service.aggregate(article)
        endtime = datetime.datetime.utcnow()

        logger.debug(
            "Total Time in milliseconds = {}".format(
                (endtime - starttime).total_seconds() * 1000
            )
        )

        topic = _service.postprocess(topic)
        return {"topic": topic}
    except Exception as e:
        raise e
