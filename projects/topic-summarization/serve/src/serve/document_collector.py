"""Trend detection."""

# Standard Library
from typing import List

import pandas as pd

# 3rd party libraries
from elasticsearch import Elasticsearch

# Source
from src.settings import get_settings

settings = get_settings()

# Source
from src.serve.utils import query_translation, topic_profile_documents_query


class DocumentCollector:
    """Package trend detection."""

    def __init__(self) -> None:
        self.es = Elasticsearch(
            [
                f"https://crawler-prod:{settings.ELASTICSEARCH_KEY.get_secret_value()}@search5-client.airpr.com"  # noqa: W505, E501
            ]
        )

    def get_documents(
        self,
        profile_id: str,
        topic_id: str,
        start_time: pd.datetime,
        end_time: pd.datetime,
    ) -> List[str]:
        """Trend detection for single topic and keyword.

        Args:
            profile_id (str): boolean query corresponding to a profile id
            topic_id (str): topic id
            start_time (pd.datetime): start time range of documents to be collected
            end_time (pd.datetime): end time range of documents to be collected
        Output:
            bool: Is there a trend corresponding to profile id and timeframe?
        """
        query = query_translation(profile_id)

        # Profile query
        results = self.es.search(
            index=settings.es_index,
            body=topic_profile_documents_query(query, start_time, end_time, topic_id),
        )
        content_list: List[str] = [
            h["_source"]["content"] for h in results["hits"]["hits"]
        ]
        return content_list[: settings.NUM_DOCUMENTS]
