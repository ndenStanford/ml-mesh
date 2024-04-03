"""Document Collector."""

# Standard Library
from typing import List

# 3rd party libraries
import pandas as pd
from elasticsearch import Elasticsearch

# Source
from src.serve.utils import query_translation, topic_profile_documents_query
from src.settings import get_settings


settings = get_settings()


class DocumentCollector:
    """Document collector class used to return documents from elastic search."""

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
        """Return documents for single topic and keyword within a timeframe.

        Args:
            profile_id (str): boolean query corresponding to a profile id
            topic_id (str): topic id
            start_time (pd.datetime): start time range of documents to be collected
            end_time (pd.datetime): end time range of documents to be collected
        Output:
            List[str]: List of content from elastic search
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
