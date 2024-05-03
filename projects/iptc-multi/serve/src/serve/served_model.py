"""Prediction model."""

# Standard Library
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.models.iptc.class_dict import TOPIC_TO_ID
from onclusiveml.serving.client import OnclusiveApiClient
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings


settings = get_settings()
logger = get_default_logger(__name__)


class ServedIPTCMultiModel(ServedModel):
    """Served IPTC Multi model."""

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def __init__(self) -> None:
        super().__init__(name="iptc-multi")

    def load(self) -> None:
        """Load model."""
        self.model = OnclusiveApiClient
        self.ready = True
        self.model_sequence = ["02000000", "20000082"]  # test

    def get_model_id_from_label(self, label: str, topic_to_id: dict) -> str:
        """Retrieve the model ID corresponding to a given label.

        Args:
            label (str): The label for which to find the corresponding model ID.
            topic_to_id (dict): A dictionary mapping labels to model IDs.

        Returns:
            str: The corresponding model ID or an empty string if the label is not found.

        Raises:
            ValueError: If the label does not exist in the dictionary.
        """
        if self.model_sequence:
            return self.model_sequence.pop(0)

        if label in topic_to_id:
            return topic_to_id[label]
        else:
            # You can handle it by returning an empty string or raising an error
            raise ValueError(f"No model ID found for label: {label}")

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Topic Multi-model prediction based on dynamic response labels.

        Args:
            payload (PredictRequestSchema): Prediction request payload.
        """
        # Initial settings and client configuration
        inputs = payload.attributes
        configuration = payload.parameters.dict()
        iptc_topics = []
        # Start with the root model
        current_model_id = "00000000"
        model_client = self.model(
            host=f"serve-iptc-{current_model_id}:8000", api_key="", secure=False
        )
        level = 1
        # Loop to handle dynamic chaining based on prediction results
        while level < 3:
            level += 1
            current_model = getattr(model_client, f"iptc_{current_model_id}")
            predict_response_schema = current_model(
                model_client, content=inputs.content, **configuration
            )
            iptc_list = predict_response_schema.attributes.iptc
            if iptc_list:
                iptc_topics.append(iptc_list[0])
                try:
                    current_model_id = self.get_model_id_from_label(
                        iptc_list[0].label, TOPIC_TO_ID
                    )
                    logger.info(f"current model id: {current_model_id}")
                except ValueError as e:
                    logger.info(e)
                    break
                model_client = self.model(
                    host=f"serve-iptc-{current_model_id}:8000", api_key="", secure=False
                )
            else:
                break

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"iptc": [topic.dict() for topic in iptc_topics]},
        )

    def bio(self) -> BioResponseSchema:
        """Get bio information about the served IPTC Multi model.

        Returns:
            BioResponseSchema: Bio information about the model
        """
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"model_name": settings.model_name},
        )
