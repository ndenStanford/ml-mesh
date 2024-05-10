"""Model."""

# Standard Library
import re
import json
from collections import Counter
from typing import Any, Dict, List, Optional, Type

# 3rd party libraries
import requests
from pydantic import BaseModel

# Internal libraries
from onclusiveml.models.multiel import BELA
from onclusiveml.nlp.language import filter_language
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.nlp.language.lang_exception import (
    LanguageDetectionException,
    LanguageFilterException,
)
from onclusiveml.serving.rest.serve import OnclusiveHTTPException, ServedModel

# Source
from src.serve.artifacts import BelaModelArtifacts
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings


settings = get_settings()


class ServedBelaModel(ServedModel):
    """Entity linking model."""

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def __init__(self, served_model_artifacts: BelaModelArtifacts):
        """Initialize the served Content Scoring model with its artifacts.
        Args:
            served_model_artifacts (BelaModelArtifacts): Served model artifact
        """
        self.served_model_artifacts = served_model_artifacts
        self._model = None
        super().__init__(name=served_model_artifacts.model_name)

    def bio(self) -> BioResponseSchema:
        """Model bio."""
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"model_name": self.name},
        )

    @property
    def model(self) -> BELA:
        """Model class."""
        if self.ready:
            return self._model
        raise ValueError(
            "Model has not been initialized. Please call .load() before making a prediction"
        )

    def load(self) -> None:
        """Load the model artifacts and prepare the model for prediction."""
        # Load model artifacts into ready CompiledContentScoring instance
        content_model_directory = self.served_model_artifacts.model_artifact_directory
        print("path: ", content_model_directory)
        self._model = BELA(
            md_threshold=0.2,
            el_threshold=0.4, 
            checkpoint_name="wiki", 
            device="cuda:0",
            config_name="joint_el_mel_new",
            repo=content_model_directory
        )
        # Load model card JSON file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True

    def entities(self) -> Optional[Dict[str, Any]]:
        """Entities to be linked."""
        return self._entities

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Prediction."""
        attributes = payload.data.attributes
        parameters = payload.data.parameters

        content = attributes.content
        lang = parameters.lang
        entities = getattr(attributes, "entities", None)  # Fetch entities if provided
        mention_offsets = getattr(attributes, "mention_offsets", None)  # Fetch mention offsets if provided
        mention_lengths = getattr(attributes, "mention_lengths", None)  # Fetch mention lengths if provided

        content = re.sub("\n+", " ", content)
        print('TEXT: ',content)
        try:
            output = self._predict(content=content, language=lang, entities=entities, mention_offsets=mention_offsets, mention_lengths=mention_lengths)
        except (
            LanguageDetectionException,
            LanguageFilterException,
        ) as language_exception:
            raise OnclusiveHTTPException(
                status_code=422, detail=language_exception.message
            )
        print('OUTPUT: ', output)
        entities = [entry["entities"] for entry in output]
        print('ENTITIES: ', entities)
        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"entities": entities},
        )

    @filter_language(supported_languages=list(LanguageIso), raise_if_none=True)
    def _predict(
        self,
        content: str,
        language: str,
        entities: Optional[List[Dict[str, Any]]],
        mention_offsets: Optional[List[List[Optional[int]]]],
        mention_lengths: Optional[List[List[Optional[int]]]],
    ) -> List[Dict[str, Any]]:
        """Language filtered prediction."""
        print('LANGUAGE: ', language)
        if entities:
            mention_offsets = []
            mention_lengths = []
            for entity in entities:
                sentence_index = entity["sentence_indexes"][0]
                mention_offsets.append([0])  # Assuming start of each sentence
                mention_lengths.append([len(entity["text"])])
            return self.model.process_disambiguation_batch(list_text=content.split(". "), mention_offsets=mention_offsets, mention_lengths=mention_lengths, entities=entities)
        elif mention_offsets and mention_lengths:
            return self.model.process_disambiguation_batch(list_text=content.split(". "), mention_offsets=mention_offsets, mention_lengths=mention_lengths, entities=[])
        else:
            return self.model.process_batch(list_text=content.split(". "))
