"""Topic handler."""

# Standard Library
import datetime
import re
from typing import Any, Dict, Optional

# 3rd party libraries
# OpenAI library
# import openai
import requests
from pydantic import BaseSettings

# Internal libraries
# Internal library
from onclusiveml.core.logging import get_default_logger


# from src.settings import Settings

# OpenAI api key

logger = get_default_logger(__name__)
# setting class


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
# openai.api_key = settings.OPENAI_API_KEY


class TopicHandler:
    """Detect trends by GPT."""

    # use gpt to generate summary on certain category; will be called in aggregate.
    def inference(
        self,
        article: list,
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
        print("-------------------")
        print("-------------------")
        print("result in inference : ", q)
        # print('\n')
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
