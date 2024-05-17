"""Model."""

# Standard Library
import datetime
from typing import Any, Dict, List, Optional, Type

# 3rd party libraries
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
        self._model = BELA(
            md_threshold=0.2,
            el_threshold=0.4,
            checkpoint_name="wiki",
            device="cuda:0",
            config_name="joint_el_mel_new",
            repo=content_model_directory,
        )
        # Load model card JSON file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True

    def entities(self) -> Optional[Dict[str, Any]]:
        """Entities to be linked."""
        return self._entities

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:  # noqa
        """Prediction."""
        attributes = payload.data.attributes
        parameters = payload.data.parameters

        content = attributes.content
        lang = parameters.lang
        entities = getattr(attributes, "entities", None)
        mention_offsets = getattr(attributes, "mention_offsets", None)
        mention_lengths = getattr(attributes, "mention_lengths", None)

        try:
            start_time = datetime.datetime.now()
            output = self._predict(
                content=content,
                language=lang,
                entities=entities,
                mention_offsets=mention_offsets,
                mention_lengths=mention_lengths,
            )
            end_time = datetime.datetime.now()
            latency = (end_time - start_time).total_seconds()
            print("Latency:", latency)
        except (
            LanguageDetectionException,
            LanguageFilterException,
        ) as language_exception:
            raise OnclusiveHTTPException(
                status_code=422, detail=language_exception.message
            )
        entities_with_links = []

        if entities:
            for sentence_idx, entry in enumerate(output):
                try:
                    entity_score_map = dict(zip(entry["entities"], entry["scores"]))
                    for idx, entity_id in enumerate(entry["entities"]):
                        start_offset = entry["offsets"][idx]
                        entity_length = entry["lengths"][idx]
                        end_offset = start_offset + entity_length
                        entity_text = str(content[start_offset:end_offset])
                        entity_with_link = {
                            "entity_text": entity_text,
                            "wiki_link": "https://www.wikidata.org/wiki/" + entity_id,
                            "wiki_score": entity_score_map.get(entity_id, None) / 100,
                        }
                        entities_with_links.append(entity_with_link)
                except KeyError as e:
                    raise KeyError(f"KeyError occurred: {e}")
                except IndexError as e:
                    raise IndexError(f"IndexError occurred: {e}")
                except Exception as e:
                    raise Exception(f"An unexpected error occurred: {e}")
        else:
            for sentence_idx, entry in enumerate(output):
                try:
                    entity_score_map = dict(zip(entry["entities"], entry["el_scores"]))
                    entity_ner_map = dict(zip(entry["entities"], entry["md_scores"]))
                    for idx, entity_id in enumerate(entry["entities"]):
                        start_offset = entry["offsets"][idx]
                        entity_length = entry["lengths"][idx]
                        end_offset = start_offset + entity_length
                        entity_text = str(content[start_offset:end_offset])
                        entity_with_link = {
                            "entity_text": entity_text,
                            "score": entity_ner_map.get(entity_id, None),
                            "sentence_indexes": [sentence_idx],
                            "wiki_link": "https://www.wikidata.org/wiki/" + entity_id,
                            "wiki_score": entity_score_map.get(entity_id, None),
                        }
                        entities_with_links.append(entity_with_link)
                except KeyError as e:
                    raise KeyError(f"KeyError occurred: {e}")
                except IndexError as e:
                    raise IndexError(f"IndexError occurred: {e}")
                except Exception as e:
                    raise Exception(f"An unexpected error occurred: {e}")

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"entities": entities_with_links},
        )

    @filter_language(supported_languages=list(LanguageIso), raise_if_none=True)
    def _predict(
        self,
        content: str,
        language: str,
        entities: Optional[List[List[Optional[int]]]],
        mention_offsets: Optional[List[List[Optional[int]]]],
        mention_lengths: Optional[List[List[Optional[int]]]],
    ) -> List[Dict[str, Any]]:
        """Language filtered prediction."""
        if mention_offsets and mention_lengths and entities:
            list_texts = [content for i in range(len(mention_offsets))]
            return self.model.process_disambiguation_batch(
                list_text=list_texts,
                mention_offsets=mention_offsets,
                mention_lengths=mention_lengths,
                entities=entities,
            )
        else:
            list_texts = [content]
            return self.model.process_batch(list_text=list_texts)
