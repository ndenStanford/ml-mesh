# type: ignore
# isort: skip_file
# black:skip_file
"""Prediction model."""

# Standard Library
from typing import Type, Optional, List, Dict, Union, Tuple
from datetime import datetime

from onclusiveml.core.base import OnclusiveBaseModel
import pandas as pd
from collections import Counter

# 3rd party libraries
from fastapi import HTTPException, status

# Internal libraries
from onclusiveml.serving.rest.serve import ServedModel
from onclusiveml.core.serialization import JsonApiSchema
from onclusiveml.core.retry import retry
from onclusiveml.core.logging import get_default_logger
from src.serve.tables import TopicSummaryDynamoDB
from src.serve.exceptions import (
    TopicSummaryInsertionException,
    TopicSummarizationParsingException,
    TopicSummarizationJSONDecodeException,
)
from onclusiveml.serving.serialization.topic_summarization.v1 import ImpactCategoryLabel

# Source
from src.serve.schema import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings

from src.serve.topic import TopicHandler
from src.serve.trend_detection import TrendDetection
from src.serve.impact_quantification import ImpactQuantification
from src.serve.document_collector import DocumentCollector
from onclusiveml.queries.query_profile import (
    StringQueryProfile,
    BaseQueryProfile,
    ProductionToolsQueryProfile,
    MediaApiStringQuery,
)

logger = get_default_logger(__name__)

settings = get_settings()


class ServedTopicModel(ServedModel):
    """Served Topic detection model."""

    predict_request_model: Type[OnclusiveBaseModel] = PredictRequestSchema
    predict_response_model: Type[OnclusiveBaseModel] = PredictResponseSchema
    bio_response_model: Type[OnclusiveBaseModel] = BioResponseSchema

    def _preprocess_string_query(self, query_string: str) -> str:
        """Pre processing of query strings."""
        preprocessed_query = query_string.replace('\\"', '"')
        return preprocessed_query

    def get_query_profile(self, inputs: JsonApiSchema) -> Optional[BaseQueryProfile]:
        """Convert user profile input into appropriate Profile class."""
        # Fake comment. Add to enforce new image build.
        if inputs.query_string:
            return StringQueryProfile(
                string_query=self._preprocess_string_query(inputs.query_string)
            )
        elif inputs.query_id:
            return ProductionToolsQueryProfile(
                version=inputs.media_api_version, query_id=inputs.query_id
            )
        elif inputs.media_api_query:
            return MediaApiStringQuery(string_query=inputs.media_api_query)
        else:
            logger.error("QueryProfile not found")
            # TODO: ADD ERROR RESPONSE HERE
            return None

    def __init__(self) -> None:
        super().__init__(name="topic-summarization")

    def load(self) -> None:
        """Load model."""
        # load model artifacts into ready CompiledKeyBERT instance
        self.model = TopicHandler()
        self.trend_detector = TrendDetection()
        self.impact_quantifier = ImpactQuantification()
        self.document_collector = DocumentCollector()
        self.ready = True

    @retry(tries=3)
    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Topic-detection prediction.

        Args:
            payload (PredictRequestModel): prediction request payload.
        """
        # extract inputs data and inference specs from incoming payload
        inputs = payload.attributes
        parameter_input = payload.parameters
        content = inputs.content
        trend_found = None
        save_report_dynamodb = inputs.save_report_dynamodb
        query_all_doc_count = None
        query_topic_doc_count = None
        sentiment_impact_flag = inputs.sentiment_impact_flag
        if not content:
            topic_id = inputs.topic_id
            query_profile = self.get_query_profile(inputs)
            # as we don't have 360 media api boolean query now, so use if as a temporary solution
            if inputs.query_string or inputs.query_id:
                boolean_query = query_profile.query
            elif inputs.media_api_query:
                boolean_query = query_profile.media_query
            trend_detection = inputs.trend_detection

            # this will function the same as `pd.Timestamp.now()` but is used to allow freeze time
            # to work for integration tests
            trend_end_time = pd.Timestamp(datetime.now())

            trend_lookback_days = (
                parameter_input.override_trend_lookback_days
                if parameter_input.override_trend_lookback_days
                else settings.TREND_LOOKBACK_DAYS
            )

            trend_start_time = trend_end_time - pd.Timedelta(days=trend_lookback_days)

            topic_document_threshold = (
                parameter_input.override_topic_document_threshold
                if parameter_input.override_topic_document_threshold
                else settings.TOPIC_DOCUMENT_THRESHOLD
            )
            trend_time_interval = (
                parameter_input.override_trend_time_interval
                if parameter_input.override_trend_time_interval
                else settings.TREND_TIME_INTERVAL
            )

            if trend_detection:
                (
                    trend_found,
                    inflection_point,
                    query_all_doc_count,
                    query_topic_doc_count,
                ) = self.trend_detector.single_topic_trend(
                    query_profile,
                    topic_id,
                    trend_start_time,
                    trend_end_time,
                    topic_document_threshold,
                    trend_time_interval,
                )

            doc_start_time = trend_start_time
            doc_end_time = trend_end_time

            days_past_inflection_point = (
                parameter_input.override_document_collector_end_date
                if parameter_input.override_document_collector_end_date
                else settings.DAYS_PAST_INFLECTION_POINT
            )

            if not trend_detection or trend_found:
                # if trending, retrieve documents between inflection point and next day
                if trend_found:
                    doc_start_time = inflection_point
                    doc_end_time = inflection_point + pd.Timedelta(
                        days=days_past_inflection_point
                    )

                # collect documents of profile
                content, lead_journalists_attributes = (
                    self.document_collector.get_documents_and_lead_journalists_attributes(
                        query_profile, topic_id, doc_start_time, doc_end_time
                    )
                )

                (
                    topic,
                    topic_summary_quality,
                ) = self.model_aggregate_and_handle_exceptions(
                    content, boolean_query, sentiment_impact_flag
                )
                impact_category = self.impact_quantifier.quantify_impact(
                    query_profile, topic_id
                )

                # retrieve lead journalists
                leading_journalists = self.retrieve_lead_journalists_if_exists(
                    lead_journalists_attributes, topic
                )

                topic["lead_journalists"] = leading_journalists
            else:
                topic = None
                impact_category = None
                topic_summary_quality = None
        else:
            topic, topic_summary_quality = self.model_aggregate_and_handle_exceptions(
                content, sentiment_impact_flag
            )
            impact_category = None
        if save_report_dynamodb:
            if inputs.query_string or inputs.query_id:
                query_string = query_profile.query
            elif inputs.media_api_query:
                query_string = query_profile.media_query
            dynamodb_dict = {
                "topic_id": topic_id,
                "trending": trend_found,
                "timestamp": datetime.now(),
                "query_id": inputs.query_id,
                "query_string": query_string,
                "analysis": topic,
                "impact_category": impact_category,
                "trend_lookback_days": trend_lookback_days,
                "topic_document_threshold": topic_document_threshold,
                "trend_time_interval": trend_time_interval,
                "days_past_inflection_point": days_past_inflection_point,
                "content": content,
                "query_all_doc_count": query_all_doc_count,
                "query_topic_doc_count": query_topic_doc_count,
                "topic_summary_quality": topic_summary_quality,
            }
            print("\n")
            print("\n")
            print("\n")
            print("DB INPUT :", dynamodb_dict)
            client = TopicSummaryDynamoDB(**dynamodb_dict)

            try:
                client.save()
            except Exception as e:
                raise TopicSummaryInsertionException(dynamodb_dict=dynamodb_dict, e=e)

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={
                "topic": topic,
                "impact_category": impact_category,
                "trending": trend_found,
                "timestamp": datetime.now(),
                "topic_summary_quality": topic_summary_quality,
            },
        )

    def model_aggregate_and_handle_exceptions(
        self,
        content: List[str],
        boolean_query: Optional[str] = None,
        sentiment_impact_flag: Optional[bool] = False,
    ) -> Tuple[
        Dict[str, Union[Dict[str, Union[str, ImpactCategoryLabel]], str, None]],
        Union[bool, None],
    ]:
        """Call model aggregate and handle exceptions.

        Args:
            content (List[str]): article content.
            boolean_query (Optional[str]): boolean query
            sentiment_impact_flag (Optional[bool]): boolean query for detecting sentiment or not
        """
        try:
            topic, topic_summary_quality = self.model.aggregate(
                content, boolean_query, sentiment_impact_flag
            )
            return topic, topic_summary_quality
        except (
            TopicSummarizationParsingException,
            TopicSummarizationJSONDecodeException,
        ) as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def bio(self) -> BioResponseSchema:
        """Model bio endpoint."""
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"model_name": settings.model_name},
        )

    def retrieve_lead_journalists_if_exists(
        self,
        lead_journalists_attributes: List[Dict],
        topic: Dict[str, Union[Dict[str, Union[str, ImpactCategoryLabel]], str, None]],
    ) -> Union[List[str], None]:
        """Determine if some articles are written by leading journalists and/or published on high tier websites.

        Args:
            lead_journalists_attributes (List[Dict]): List of Dicts containing attributes that can help determine
            if lead journalists exists.
            topic (Dict[str, Union[Dict[str, Union[str, ImpactCategoryLabel]], str, None]]): topic for
            citations filtering
        """
        try:
            # check for authors with frequent cited articles in the topic summaries
            citations_list = []
            themes = [
                "opportunities",
                "risk",
                "threats",
                "company",
                "brand",
                "ceo",
                "customer",
                "stock",
                "industry",
                "environment",
            ]
            for theme in themes:
                citations = topic[theme]["sources"].split(",")
                logger.debug(f"citations : {citations}")
                citations = [int(c.strip()) for c in citations if c and c.isdigit()]
                citations_list += citations

            citations_frequency = Counter(citations_list)
            # TODO filter citations above thresh
            citations_frequency = {
                c: f
                for c, f in citations_frequency.items()
                if f >= settings.CITATIONS_THRESHOLD
            }
            logger.debug(f"citations frequency : {citations_frequency} {topic.keys()}")

            author_list = []
            high_pagerank_authors = {}
            top_publication_tier_authors = {}
            valid_authors = []
            most_cited_authors = {}
            for i, attributes in enumerate(lead_journalists_attributes):

                author = attributes.get("author", "").strip()
                # if author name is empty or unkown continue
                if not author or "unkown" in author.lower():
                    continue

                author_list.append(author)

                # add author to list of most cited if its ids in citations frequency
                if i in citations_frequency:
                    most_cited_authors[author] = citations_frequency[i]

                is_valid_author = attributes.get("is_valid_author", False)
                if is_valid_author:
                    valid_authors.append(author)

                pagerank = attributes.get("pagerank", 0)
                # Check if pagerank is above threshold to add it to
                if pagerank >= settings.PAGE_RANK_THRESHOLD:
                    logger.debug(
                        f"pagerank {pagerank} is above threshold {settings.PAGE_RANK_THRESHOLD}"
                    )

                    if (
                        author not in high_pagerank_authors
                        or pagerank > high_pagerank_authors[author]
                    ):
                        high_pagerank_authors[author] = pagerank

            publication_tier = attributes.get("publication_details.publication_tier", 5)
            # Check if publication tier is lower than or equal the threshold
            if publication_tier < settings.PUBLICATION_TIER_THRESHOLD:
                logger.debug(
                    f"publication tier {publication_tier} is below threshold {settings.PUBLICATION_TIER_THRESHOLD}"
                )
                if (
                    author not in top_publication_tier_authors
                    or publication_tier < top_publication_tier_authors[author]
                ):
                    top_publication_tier_authors[author] = publication_tier

            # count the frequency of each author
            author_frequency = Counter(author_list)
            # filter frequent authors
            frequent_authors = {
                auth: freq
                for auth, freq in author_frequency.items()
                if freq >= settings.AUTHOR_FREQUENCY_THRESHOLD
            }

            logger.debug(f"Frequent authors: {frequent_authors}")
            logger.debug(f"High pagerank authors : {high_pagerank_authors}")
            logger.debug(
                f"Top publication tier authors : {top_publication_tier_authors}"
            )
            logger.debug(f"Most cited authors: {most_cited_authors}")

            # get the union of the lists of authors filtered by each criteria
            lead_journalists = list(
                set().union(
                    frequent_authors,
                    high_pagerank_authors,
                    top_publication_tier_authors,
                    most_cited_authors,
                )
            )

            # TODO do intersection to valid authors to

            logger.debug(f"lead journalists: {lead_journalists}")

            return lead_journalists
        except Exception as e:
            logger.error(e)
            return []
