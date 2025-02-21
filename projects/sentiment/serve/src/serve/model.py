"""Prediction model."""

# Standard Library
import re
from typing import Any, Dict, List, Optional, Type

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
from onclusiveml.models.sentiment import TrainedSentiment
from onclusiveml.nlp.language import filter_language
from onclusiveml.nlp.language.lang_exception import (
    LanguageDetectionException,
    LanguageFilterException,
)
from onclusiveml.serving.rest.serve import OnclusiveHTTPException, ServedModel

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings


settings = get_settings()


class ServedSentModel(ServedModel):
    """Served Sent model.

    Attributes:
        predict_request_model (Type[OnclusiveBaseModel]):  Request model for prediction
        predict_response_model (Type[OnclusiveBaseModel]): Response model for prediction
        bio_response_model (Type[OnclusiveBaseModel]): Response model for bio
    """

    predict_request_model: Type[OnclusiveBaseModel] = PredictRequestSchema
    predict_response_model: Type[OnclusiveBaseModel] = PredictResponseSchema
    bio_response_model: Type[OnclusiveBaseModel] = BioResponseSchema

    def __init__(self, served_model_artifacts: ServedModelArtifacts):
        """Initalize the served Sent model with its artifacts.

        Args:
            served_model_artifacts (ServedModelArtifacts): Served model artifact
        """
        self.served_model_artifacts = served_model_artifacts
        self._model = None
        super().__init__(name=served_model_artifacts.model_name)
        # self.load()  # FOR LOCAL TESTING ONLY, REMOVE FOR PRODUCTION

    @property
    def model(self) -> TrainedSentiment:
        """Model class."""
        if self.ready:
            return self._model
        raise ValueError(
            "Model has not been initialized. Please call .load() before making a prediction"
        )

    def load(self) -> None:
        """Load the model artifacts and prepare the model for prediction."""
        # load model artifacts into ready TrainedSentiment instance
        self._model = TrainedSentiment.from_pretrained(
            self.served_model_artifacts.model_artifact_directory
        )
        # load model card json file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True

    def validate_content(self, content: str) -> bool:
        """Validate quality of input.

        Args:
            content (str): the requested string to run SA on

        Returns:
            bool: whether quality of input is good or not
        """
        # removes all punctuation
        content_without_punctuation = re.sub(r"[^\w\s]", "", content).strip()
        content_without_punctuation = " ".join(content_without_punctuation.split())
        # Check if the length of content without punctuation is at least the threshold
        if len(content_without_punctuation) < settings.MIN_CHARACTERS:
            return False

        return True

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Make predictions using the loaded Sent model.

        Args:
            payload (PredictRequestSchema): The input data for making predictions

        Returns:
            PredictResponseSchema: Response containing extracted entities
        """
        attributes = payload.attributes
        parameters = payload.parameters
        # Check if entities are provided and prepare them
        entities = attributes.entities
        if entities:
            entities = [dict(e) for e in entities]
        # Execute sentiment analysis in a language-aware context
        # validate content
        if not self.validate_content(attributes.content):
            raise OnclusiveHTTPException(
                status_code=204, detail="Content too short or contains no letters."
            )
        try:
            sentiment = self._sentiment_analysis(
                content=attributes.content,
                entities=entities,
                language=parameters.language,
                additional_params=parameters.model_dump(),
            )
        except (
            LanguageDetectionException,
            LanguageFilterException,
        ) as language_exception:
            raise OnclusiveHTTPException(
                status_code=204, detail=language_exception.message
            )
        # Prepare the response attributes
        attributes = {
            "label": sentiment.get("label"),
            "negative_prob": sentiment.get("negative_prob"),
            "positive_prob": sentiment.get("positive_prob"),
            "entities": sentiment.get("entities"),
        }

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes=attributes,
        )

    @filter_language(
        supported_languages=settings.supported_languages,
        raise_if_none=True,
    )
    def _sentiment_analysis(
        self,
        content: str,
        language: str,
        entities: Optional[List[Dict[str, Any]]],
        additional_params: dict,
    ) -> Dict[str, Any]:
        """Perform sentiment analysis considering language restrictions.

        Args:
            content (str): The text content to analyze.
            entities (Optional[List[Dict[str, Any]]]): Detected entities to consider in analysis.
            language (str): The language of the text.
            additional_params (dict): Additional parameters for model configuration.

        Returns:
            Dict[str, Any]: A dictionary containing sentiment analysis results.
        """
        return self.model(sentences=content, entities=entities, **additional_params)

    def bio(self) -> BioResponseSchema:
        """Get bio information about the served Sentiment model.

        Returns:
            BioResponseModel: Bio information about the model
        """
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=self.name,
            attributes={"model_name": self.name, "model_card": self.model_card},
        )
