# type: ignore
# isort: skip_file
# black:skip_file
"""Prediction model."""

# Standard Library
from typing import Type, Optional
from datetime import datetime

# 3rd party libraries
from pydantic import BaseModel
import pandas as pd

# Internal libraries
from onclusiveml.serving.rest.serve import ServedModel
from onclusiveml.core.serialization import JsonApiSchema
from onclusiveml.core.retry import retry
from onclusiveml.core.logging import get_default_logger

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
from onclusiveml.data.query_profile import (
    StringQueryProfile,
    BaseQueryProfile,
    ProductionToolsQueryProfile,
)

logger = get_default_logger(__name__)

settings = get_settings()


class ServedTopicModel(ServedModel):
    """Served Topic detection model."""

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def get_query_profile(self, inputs: JsonApiSchema) -> Optional[BaseQueryProfile]:
        """Convert user profile input into appropriate Profile class."""
        if inputs.query_string:
            return StringQueryProfile(string_query=inputs.query_string)
        elif inputs.query_id:
            return ProductionToolsQueryProfile(
                version=inputs.media_api_version, query_id=inputs.query_id
            )
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
        content = inputs.content

        if not content:
            topic_id = inputs.topic_id
            query_profile = self.get_query_profile(inputs)
            trend_detection = inputs.trend_detection

            # this will function the same as `pd.Timestamp.now()` but is used to allow freeze time
            # to work for integration tests
            end_time = pd.Timestamp(datetime.now())
            start_time = end_time - pd.Timedelta(days=settings.trend_lookback_days)
            trending = False
            if trend_detection:
                trending, inflection_point = self.trend_detector.single_topic_trend(
                    query_profile, topic_id, start_time, end_time
                )
                print("&" * 30)
                print(trending)
                print(inflection_point)
            if not trend_detection or trending:
                # if trending, retrieve documents between inflection point and next day
                if trending:
                    start_time = inflection_point
                    end_time = start_time + pd.Timedelta(days=1)

                # collect documents of profile
                content = self.document_collector.get_documents(
                    query_profile, topic_id, start_time, end_time
                )
                print("&" * 30)
                print(content)
                topic = self.model.aggregate(content)
                print("topic")
                print(topic)
                impact_category = self.impact_quantifier.quantify_impact(
                    query_profile, topic_id
                )
                print("impact_category")
                print(impact_category)
            else:
                topic = None
                impact_category = None
        else:
            topic = self.model.aggregate(content)
            impact_category = None

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"topic": topic, "impact_category": impact_category},
        )

    def bio(self) -> BioResponseSchema:
        """Model bio endpoint."""
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"model_name": settings.model_name},
        )
