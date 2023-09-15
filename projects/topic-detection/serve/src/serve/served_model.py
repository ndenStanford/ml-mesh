# isort: skip_file
# black:skip_file
"""Prediction model."""

# Standard Library
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.serve.server_models import (
    BioResponseModel,
    PredictRequestModel,
    PredictResponseModel,
)

# from onclusiveml.syndicate.datasketch.topic import TopicHandler#?
from src.serve.topic import TopicHandler


class ServedTopicModel(ServedModel):
    """Served Topic detection model."""

    predict_request_model: Type[BaseModel] = PredictRequestModel
    predict_response_model: Type[BaseModel] = PredictResponseModel
    bio_response_model: Type[BaseModel] = BioResponseModel

    def __init__(self) -> None:
        super().__init__(name="topic-detection")

    def load(self) -> None:
        """Load model."""
        # load model artifacts into ready CompiledKeyBERT instance
        self.model = TopicHandler()
        self.ready = True
        self.model_card = BioResponseModel(model_name="topic-detection")

    def predict(self, payload: PredictRequestModel) -> PredictResponseModel:
        """Topic-detection prediction.

        Args:
            payload (PredictRequestModel): prediction request payload.
        """
        # extract inputs data and inference specs from incoming payload
        inputs = payload.inputs
        # configuration = payload.configuration
        content = inputs.content
        industry = inputs.industry

        article = self.model.pre_process(content)
        topic = self.model.aggregate(article, industry)

        return PredictResponseModel(topic=topic)

    def bio(self) -> BioResponseModel:
        """Model bio endpoint."""
        return self.model_card
