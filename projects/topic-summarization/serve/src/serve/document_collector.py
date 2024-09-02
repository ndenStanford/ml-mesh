"""Document Collector."""

# isort: skip_file

# Standard Library
from typing import List
from datetime import datetime

# 3rd party libraries
from elasticsearch import Elasticsearch

# Internal libraries
from onclusiveml.queries.query_profile import BaseQueryProfile, MediaAPISettings

# Source
from src.serve.utils import topic_profile_documents_query
from src.settings import get_settings

settings = get_settings()


class DocumentCollector:
    """Document collector class used to return documents from elastic search."""

    def __init__(self) -> None:
        self.es = Elasticsearch(
            [
                f"https://crawler-prod:{settings.ELASTICSEARCH_KEY.get_secret_value()}@search5-client.airpr.com"  # noqa: W505, E501
            ],
            timeout=settings.ES_TIMEOUT,
        )
        self.es_index = settings.es_index

    def get_documents(
        self,
        query_profile: BaseQueryProfile,
        topic_id: str,
        start_time: datetime,
        end_time: datetime,
    ) -> List[str]:
        """Return documents for single topic and keyword within a timeframe.

        Args:
            query_profile (BaseQueryProfile): boolean query of a profile e.g. a company
            topic_id (str): topic id
            start_time (datetime): start time range of documents to be collected
            end_time (datetime): end time range of documents to be collected
        Output:
            List[str]: List of content from elastic search
        """
        query = query_profile.es_query(MediaAPISettings())
        # Profile query
        results = self.es.search(
            index=self.es_index,
            body=topic_profile_documents_query(
                query, start_time, end_time, topic_id, settings.NUM_DOCUMENTS
            ),
        )
        content_list: List[str] = [
            h["_source"]["content"] for h in results["hits"]["hits"]
        ]
        return content_list
