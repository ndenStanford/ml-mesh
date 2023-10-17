"""Topic handler."""
# isort: skip_file

# Standard Library
import datetime
import re
from typing import Any, Dict, List

# 3rd party libraries
# OpenAI library
# import openai
import requests

# Internal libraries
# Internal library
from onclusiveml.core.logging import get_default_logger

# Source
from src.serve._init import Settings

# from pydantic import BaseSettings


# OpenAI api key

logger = get_default_logger(__name__)
# setting class
settings = Settings()


class TopicHandler:
    """Detect trends by GPT."""

    # use gpt to generate summary on certain category; will be called in aggregate.
    def inference(
        self,
        article: List[str],
        cate: str,
        industry: str,
    ) -> str:
        """Topic detection handler method.

        Args:
            article (list): list of str
            cate (str): target category, one of ['Risk detection', 'Opportunities',
            'Threats for the brand','Company or spokespersons', 'Brand Reputation',
            'CEO Reputation', 'Customer Response', 'Stock Price Impact',
            'Industry trends']
            industry: target industry
        """
        try:
            alias = settings.PROMPT_DICT["analysis"]["alias"]
        except KeyError:
            logger.errror("Topic function not supported.")
        # transfer article to the format used in prompt
        processed_article = ""
        for i in range(len(article)):
            text = article[i]
            processed_article += (
                "\n    Article " + str(i) + ": '''" + text + "''' " + "\n"
            )

        input_dict = {
            "target_industry": industry,
            "target_category": cate,
            "content": processed_article,
        }  # input target category & articles
        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/api/v1/prompts/{}/generate".format(settings.PROMPT_API, alias),
            headers=headers,
            json=input_dict,
        )
        return eval(q.content)["generated"]

    def aggregate(self, article: list, industry: str) -> dict:
        """Function for spliting the articles into groups, then aggregate together."""
        num_article = len(article)
        n = 3  # group size
        art_index = 0
        category_list = settings.CATEGORY_LIST
        record = {cate: "" for cate in category_list}
        # do topic analysis for each category
        for cate in category_list:
            # print('current category : ', cate)
            record_cate = []
            # divide the articles into groups and summarize each group
            while art_index < num_article:
                end_index = min(art_index + n, num_article)
                input_article = article[art_index:end_index]  # E203
                res_now = self.inference(input_article, cate, industry)
                record_cate.append(res_now)
                art_index += n

            processed_summary = ""
            for i in range(len(record_cate)):
                text = record_cate[i]
                processed_summary += (
                    "\n    Summary " + str(i) + ": '''" + text + "''' " + "\n"
                )

            try:
                alias = settings.PROMPT_DICT["aggregate"]["alias"]
            except KeyError:
                logger.errror("Topic function not supported.")

            input_dict = {
                "target_industry": industry,
                "target_category": cate,
                "Summary": processed_summary,
            }  # input target category & articles
            headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

            q = requests.post(
                "{}/api/v1/prompts/{}/generate".format(settings.PROMPT_API, alias),
                headers=headers,
                json=input_dict,
            )

            record[cate] = eval(q.content)["generated"]
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
        industry = data["industry"]  # ?

        if content is None or content == "":
            logger.warning(
                "Content field is empty. This will result in no summary being returned"
            )

        article = _service.pre_process(content)  # ?

        starttime = datetime.datetime.utcnow()
        topic = _service.aggregate(article, industry)
        endtime = datetime.datetime.utcnow()

        logger.debug(
            "Total Time in milliseconds = {}".format(
                (endtime - starttime).total_seconds() * 1000
            )
        )

        topic = _service.postprocess(topic)  # ?
        return {"topic": topic}
    except Exception as e:
        raise e
