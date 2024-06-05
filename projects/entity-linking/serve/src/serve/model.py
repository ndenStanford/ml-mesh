"""Model."""

# Standard Library
import re
from typing import Any, Dict, List, Optional, Tuple, Type

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
from src.serve.artifacts import ServedModelArtifacts
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

    def __init__(self, served_model_artifacts: ServedModelArtifacts):
        """Initialize the served Content Scoring model with its artifacts.

        Args:
            served_model_artifacts (ServedModelArtifacts): Served model artifact
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
            md_threshold=settings.md_threshold,
            el_threshold=settings.el_threshold,
            checkpoint_name=settings.checkpoint_name,
            device=settings.device,
            config_name=settings.config_name,
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

        try:
            entities_with_links = self._predict(
                content=content,
                language=lang,
                entities=entities,
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
            attributes={"entities": entities_with_links},
        )

    @filter_language(
        supported_languages=list(LanguageIso),
        raise_if_none=True,
    )
    def _predict(
        self,
        content: str,
        language: str,
        entities: Optional[List[Dict[str, Any]]],
    ) -> List[Dict[str, Any]]:
        """Language filtered prediction."""
        return self._get_entity_linking(content=content, entities=entities)

    def _generate_offsets(
        self, text: str, entities: List[Dict[str, Any]]
    ) -> Tuple[List[str], List[int], List[int], List[int]]:
        """Generate a component of query to be consumed by the entity fish endpoint.

        Args:
            text (str): text to be wiki linked
            entities (List[Dict[str, Any]]):
                entities within text recognized by an external NER model
        """
        unique_entity_text = list(
            set(entity.get("entity_text", entity.get("text")) for entity in entities)
        )
        entities_offsets = []
        entities_list = []
        mention_offsets = []
        mention_lengths = []
        for entity_text in unique_entity_text:
            matched_entities = list(re.finditer(entity_text, text))
            spans = [m.span() for m in matched_entities]
            for span in spans:
                offset_start, offset_end = span
                length = offset_end - offset_start
                entities_list.append(entity_text)
                entities_offsets.append(0)
                mention_offsets.append(offset_start)
                mention_lengths.append(length)
        return entities_list, entities_offsets, mention_offsets, mention_lengths

    def _get_entity_linking(
        self,
        content: str,
        entities: Optional[List[Dict[str, Any]]],
    ) -> List[Dict[str, Any]]:
        """Get entity linking prediction."""
        entities_with_links = []
        if entities:
            (
                unique_entities_list,
                entities_offsets,
                mention_offsets,
                mention_lengths,
            ) = self._generate_offsets(text=content, entities=entities)
            output = self.model.process_disambiguation_batch(
                list_text=[content],
                mention_offsets=[mention_offsets],
                mention_lengths=[mention_lengths],
                entities=[entities_offsets],
            )
            for entity in entities:
                try:
                    if entity["entity_text"] in unique_entities_list:
                        index = unique_entities_list.index(
                            entity["entity_text"]
                        )  # noqa
                        entity_with_link = entity
                        entity_with_link["wiki_link"] = (
                            "https://www.wikidata.org/wiki/"
                            + output[0]["entities"][index]
                        )
                        entities_with_links.append(entity_with_link)
                except KeyError as e:
                    raise KeyError(f"KeyError occurred: {e}")
                except IndexError as e:
                    raise IndexError(f"IndexError occurred: {e}")
                except Exception as e:
                    raise Exception(f"An unexpected error occurred: {e}")

        else:
            list_texts = [content]
            output = self.model.process_batch(list_text=list_texts)
            try:
                entity_ner_map = dict(
                    zip(output[0]["entities"], output[0]["md_scores"])
                )
                for idx, entity_id in enumerate(output[0]["entities"]):
                    start_offset = output[0]["offsets"][idx]
                    entity_length = output[0]["lengths"][idx]
                    end_offset = start_offset + entity_length
                    entity_text = str(content[start_offset:end_offset])
                    entity_with_link = {
                        "entity_type": None,
                        "entity_text": entity_text,
                        "score": entity_ner_map.get(entity_id, None),
                        "sentence_index": [0],
                        "wiki_link": "https://www.wikidata.org/wiki/" + entity_id,
                    }
                    entities_with_links.append(entity_with_link)
            except KeyError as e:
                raise KeyError(f"KeyError occurred: {e}")
            except IndexError as e:
                raise IndexError(f"IndexError occurred: {e}")
            except Exception as e:
                raise Exception(f"An unexpected error occurred: {e}")
        return entities_with_links
