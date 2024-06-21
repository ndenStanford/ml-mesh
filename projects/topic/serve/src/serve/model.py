"""Prediction model."""

# Standard Library
from typing import Tuple, Type

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
from onclusiveml.models.topic import TrainedTopic
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


class ServedTopicModel(ServedModel):
    """Served Topic model.

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
    def model(self) -> TrainedTopic:
        """Model class."""
        if self.ready:
            return self._model
        raise ValueError(
            "Model has not been initialized. Please call .load() before making a prediction"
        )

    def load(self) -> None:
        """Load the model artifacts and prepare the model for prediction."""
        # load model artifacts into ready CompiledSent instance
        self._model = TrainedTopic.from_pretrained(
            self.served_model_artifacts.model_artifact_directory
        )
        # load model card json file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Make predictions using the loaded topic model.

        Args:
            payload (PredictRequestSchema): The input data for making predictions

        Returns:
            PredictResponseSchema: Response containing topic prediction
        """
        # content and configuration from payload
        attributes = payload.attributes
        parameters = payload.parameters
        try:
            topic_prediction = self._topic_predict(
                content=attributes.content, language=parameters.language
            )
        except (
            LanguageDetectionException,
            LanguageFilterException,
        ) as language_exception:
            raise OnclusiveHTTPException(
                status_code=204, detail=language_exception.message
            )
        attributes = {
            "topic_id": str(topic_prediction[0][0]),
            "topic_representation": [i[0] for i in topic_prediction[1]],
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
    def _topic_predict(self, content: str, language: str) -> Tuple:
        """Perform topic prediction considering language restrictions.

        Args:
            content (str): The text content to analyze.
            language (str): The language of the text.

        Returns:
            Dict[str, Any]: A dictionary containing topic prediction results.
        """
        return self.model(text=content)

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
