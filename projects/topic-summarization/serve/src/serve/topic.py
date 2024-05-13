"""Topic handler."""
# isort: skip_file

# Standard Library
import re
from typing import List, Dict, Optional, Any, Union

# 3rd party libraries
import requests
import json
from multiprocessing import Pool, cpu_count

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.preprocess import remove_html, remove_whitespace

# Source
from src.settings import get_api_settings, get_settings  # type: ignore[attr-defined]

logger = get_default_logger(__name__)
settings = get_api_settings()
model_settings = get_settings()
num_process = min(model_settings.MULTIPROCESS_WORKER, cpu_count())


class TopicHandler:
    """Topic summarization with prompt backend."""

    def inference(
        self,
        article: List[str],
        category: str,
    ) -> Optional[str]:
        """Topic summarization for single category.

        Args:
            article (list): list of str
            category (str): target category, one of ['Risk detection', 'Opportunities',
            'Threats for the brand','Company or spokespersons', 'Brand Reputation',
            'CEO Reputation', 'Customer Response', 'Stock Price Impact',
            'Industry trends', 'Environmental, social and governance']
        Output:
            Category summary: str
        """
        alias = settings.PROMPT_ALIAS["single_topic"]
        # transfer article to the format used in prompt
        processed_article = ""
        for i in range(len(article)):
            text = article[i]
            processed_article += (
                "\n    Article " + str(i) + ": '''" + text + "''' " + "\n"
            )

        input_dict = {
            "input": {
                "target_category": category,
                "content": processed_article,
            },
            "output": settings.SINGLE_TOPIC_OUTPUT_SCHEMA,
        }

        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/prompt/api/v2/prompts/{}/generate/model/{}".format(
                settings.PROMPT_API, alias, settings.DEFAULT_MODEL
            ),
            headers=headers,
            json=input_dict,
        )

        output_content = json.loads(q.content)

        return output_content.get("summary")

    def summary(
        self,
        article: List[str],
    ) -> str:
        """Summarize multiple articles.

        Args:
            article (list): list of str
        Output:
            Summary: str
        """
        alias = settings.PROMPT_ALIAS["single_summary"]
        # transfer article to the format used in prompt
        processed_article = ""
        for i in range(len(article)):
            text = article[i]
            processed_article += (
                "\n    Article " + str(i) + ": '''" + text + "''' " + "\n"
            )

        input_dict = {
            "input": {
                "content": processed_article,
            },
            "output": settings.SINGLE_SUMMARY_OUTPUT_SCHEMA,
        }

        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/prompt/api/v2/prompts/{}/generate/model/{}".format(
                settings.PROMPT_API, alias, settings.DEFAULT_MODEL
            ),
            headers=headers,
            json=input_dict,
        )

        return json.loads(q.content)

    def summary_aggregate(self, grouped_article: List[List]) -> Dict[str, str]:
        """Function for aggregating summaries and generating theme.

        Args:
            grouped_article (list): list of list
        Output:
            summary & theme (dict): Dict[str, str]
        """
        record = {}
        combined_input = [(item) for item in grouped_article]

        # parallel based on grouped article
        with Pool(processes=num_process) as p:
            group_summary = p.map(self.summary, combined_input)  # list of tupel

        processed_summary = "\n".join(
            [
                f"summary {index + 1}: '''{article}'''"
                for index, article in enumerate(group_summary)
            ]
        )

        alias = settings.PROMPT_ALIAS["summary_aggregation"]
        input_dict = {
            "input": {"summary": processed_summary},
            "output": settings.SUMMARY_AGGREGATION_OUTPUT_SCHEMA,
        }
        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/prompt/api/v2/prompts/{}/generate/model/{}".format(
                settings.PROMPT_API, alias, settings.DEFAULT_MODEL
            ),
            headers=headers,
            json=input_dict,
        )

        output_content = json.loads(q.content)
        record["summary"] = output_content["summary"]
        record["theme"] = output_content["theme"]

        return record

    def process_category(self, grouped_article: List[List], category: str) -> tuple:
        """Function to prepare parallel based on category.

        From all input articles to final analyze for the category

        Args:
            grouped_article: list of list of str, all articles
            category: str
        Output:
            a tuple with summary, impact and theme.
        """
        record_cate = []
        for input_article in grouped_article:
            res_now = self.inference(input_article, category)
            record_cate.append(res_now)

        # combine the output of each group together
        processed_summary = "\n".join(
            [
                f"summary {index + 1}: '''{article}'''"
                for index, article in enumerate(record_cate)
            ]
        )

        alias = settings.PROMPT_ALIAS["topic_aggregation"]

        input_dict = {
            "input": {
                "target_category": model_settings.IMPACT_CATEGORIES[category],
                "summary": processed_summary,
            },
            "output": settings.TOPIC_AGGREGATION_OUTPUT_SCHEMA,
        }

        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/prompt/api/v2/prompts/{}/generate/model/{}".format(
                settings.PROMPT_API, alias, settings.DEFAULT_MODEL
            ),
            headers=headers,
            json=input_dict,
        )

        output_content = json.loads(q.content)
        agg_out_content, agg_out_impact, agg_out_theme = (
            output_content["summary"],
            output_content["impact"],
            output_content["theme"],
        )
        return agg_out_content, agg_out_impact, agg_out_theme

    def topic_aggregate(
        self, grouped_article: List[List]
    ) -> Dict[str, Optional[Dict[str, str]]]:
        """Function for aggregating topic analysis, and generate theme and impact level.

        Args:
            grouped_article(list): list of str
        Output:
            topic analysis & topic theme & topic impact(dict): dict[str,str]
        """
        record: Dict[str, Optional[Dict[str, Any]]] = {}  # record for final output

        combined_input = [
            (grouped_article, key) for key in model_settings.IMPACT_CATEGORIES
        ]
        # parallel based on category
        with Pool(processes=num_process) as p:
            category_summary = p.starmap(
                self.process_category, combined_input
            )  # list of tupel

        # combine the final result
        for i, key in enumerate(model_settings.IMPACT_CATEGORIES):
            agg_out_content, agg_out_impact, agg_out_theme = (
                category_summary[i][0],
                category_summary[i][1],
                category_summary[i][2],
            )
            if not agg_out_content:
                continue
            record[key] = {
                "name": model_settings.IMPACT_CATEGORIES[key],
                "analysis": agg_out_content,
                "theme": agg_out_theme,
                "impact": agg_out_impact,
            }

        return record

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

    def group(self, article: List[str]) -> List[List]:
        """Divide articles into groups.

        Args:
            article(list): list of str
        Output:
            grouped articles: List[List[str]]
        """
        num_article = len(article)
        n = model_settings.ARTICLE_GROUP_SIZE  # group size
        art_index = 0
        grouped = []
        while art_index < num_article:
            end_index = min(art_index + n, num_article)
            grouped.append(article[art_index:end_index])  # E203
            art_index += n
        return grouped

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
        grouped_article = self.group(article)
        topic_result = self.topic_aggregate(grouped_article)
        summary_result = self.summary_aggregate(grouped_article)
        merged_result: Dict[str, Union[Dict[str, str], str, None]] = {}
        merged_result.update(topic_result)
        merged_result.update(summary_result)
        return merged_result
