"""Prediction model."""

# Standard Library
from typing import Any, Dict, List, Type

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
from onclusiveml.models.ner import CompiledNER
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


class ServedNERModel(ServedModel):
    """Served NER model.

    Attributes:
        predict_request_model (Type[OnclusiveBaseModel]):  Request model for prediction
        predict_response_model (Type[OnclusiveBaseModel]): Response model for prediction
        bio_response_model (Type[OnclusiveBaseModel]): Response model for bio
    """

    predict_request_model: Type[OnclusiveBaseModel] = PredictRequestSchema
    predict_response_model: Type[OnclusiveBaseModel] = PredictResponseSchema
    bio_response_model: Type[OnclusiveBaseModel] = BioResponseSchema

    def __init__(self, served_model_artifacts: ServedModelArtifacts):
        """Initalize the served NER model with its artifacts.

        Args:
            served_model_artifacts (ServedModelArtifacts): Served model artifact
        """
        self.served_model_artifacts = served_model_artifacts
        self._model = None
        super().__init__(name=served_model_artifacts.model_name)

    @property
    def model(self) -> CompiledNER:
        """Model class."""
        if self.ready:
            return self._model
        raise ValueError(
            "Model has not been initialized. Please call .load() before making a prediction"
        )

    def load(self) -> None:
        """Load the model artifacts and prepare the model for prediction."""
        # load model artifacts into ready CompiledNER instance
        self._model = CompiledNER.from_pretrained(
            self.served_model_artifacts.model_artifact_directory
        )
        # load model card json file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True

    @filter_language(
        supported_languages=settings.supported_languages,
        raise_if_none=True,
    )
    def _predict(
        self,
        content: str,
        language: str,
        additional_params: dict,
    ) -> List[List[Dict[str, Any]]]:
        """Make NER predictions considering language and additional parameters.

        Args:
            content (str): The text content to analyze.
            language (str): The language of the text.
            additional_params (dict): Additional parameters for model configuration.

        Returns:
            List[List[Dict[str, Any]]]: List of extracted named entities in dictionary format.
        """
        return self.model(documents=content, **additional_params)

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Make predictions using the loaded NER model.

        Args:
            payload (PredictRequestSchema): The input data for making predictions

        Returns:
            PredictResponseSchema: Response containing extracted entities
        """
        # attributes and parameters from payload
        attributes = payload.attributes
        parameters = payload.parameters

        if attributes.content == "":
            entities_list: list = [[]]
        else:
            try:
                # score the model
                entities_list = self._predict(
                    content=[attributes.content],
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
        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={
                "entities": [
                    entity._asdict()
                    for entities in entities_list
                    for entity in entities
                ]
            },
        )

    def bio(self) -> BioResponseSchema:
        """Get bio information about the served NER model.

        Returns:
            BioResponseModel: Bio information about the model
        """
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=self.name,
            attributes={"model_name": self.name, "model_card": self.model_card},
        )
