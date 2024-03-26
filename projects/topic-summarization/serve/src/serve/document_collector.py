"""Trend detection."""

# Standard Library
from typing import Any, List

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
        self, profile_id: Any, topic_id: Any, start_time: Any, end_time: Any
    ) -> List[str]:
        """Trend detection for single topic and keyword.

        Args:
            profile_id (Any): boolean query
            topic_id (Any): topic id
            start_time (Any): start time range of documents to be collected
            end_time (Any): end time range of documents to be collected
        Output:
            bool: trend or not
        """
        query = query_translation(profile_id)

        # Profile query
        results = self.es.search(
            index=settings.es_index,
            body=topic_profile_documents_query(query, start_time, end_time, topic_id),
        )
        content_list: List[str] = [
            h["_source"]["title"] for h in results["hits"]["hits"]
        ]
        return content_list[: settings.NUM_DOCUMENTS]
