"""Document Collector."""

# isort: skip_file

# Standard Library
from typing import List, Dict
from datetime import datetime

# 3rd party libraries
from elasticsearch import Elasticsearch

# Internal libraries
from onclusiveml.queries.query_profile import BaseQueryProfile, MediaAPISettings
from onclusiveml.core.logging import get_default_logger

# Source
from src.serve.utils import topic_profile_documents_query
from src.settings import get_settings

settings = get_settings()
logger = get_default_logger(__name__)


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

    def get_documents_and_lead_journalists_attributes(
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
        """
        "author", "author_canonical_name", "is_verified_author", "is_valid_author",
        "verified_author.canon_name", "verified_author.reach", "verified_author.subjects",
        "verified_author.full_name", "verified_author.title", "pagerank", "publication_details.publication_tier",
        "publication_details.publication_type", "moreover_publication.editorial_rank",
        "moreover_publication.feed_rank", "domain_details.global_rank", "social_counts.total_shares"
        """
        # print(results["hits"]["hits"][0]["_source"])
        lead_journalists_attributes_list: List[Dict] = []
        for h in results["hits"]["hits"]:
            logger.debug(f'hit url : {h["_source"]["url"]}')
            attributes: Dict = {}
            for attr in settings.LEAD_JOURNALISTS_ATTRIBUTES:
                if attr in h["_source"]:
                    attributes[attr] = h["_source"][attr]
                elif "." in attr:
                    attr_split = attr.split(".")
                    if (
                        attr_split[0] in h["_source"]
                        and attr_split[1] in h["_source"][attr_split[0]]
                    ):
                        attributes[attr] = h["_source"][attr_split[0]][attr_split[1]]
            lead_journalists_attributes_list.append(attributes)

        logger.debug(f"articles count : {len(content_list)}")
        logger.debug(
            f"lead_journalists_attributes_list : {lead_journalists_attributes_list}"
        )

        return content_list, lead_journalists_attributes_list
