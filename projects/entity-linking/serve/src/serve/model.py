"""Model."""

# Standard Library
import re
from typing import Any, Dict, List, Optional, Tuple, Type

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
from onclusiveml.models.multiel import BELA
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


class ServedBelaModel(ServedModel):
    """Entity linking model."""

    predict_request_model: Type[OnclusiveBaseModel] = PredictRequestSchema
    predict_response_model: Type[OnclusiveBaseModel] = PredictResponseSchema
    bio_response_model: Type[OnclusiveBaseModel] = BioResponseSchema

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
        supported_languages=settings.supported_languages,
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
    ) -> Tuple[List[Optional[str]], List[int], List[int], List[int]]:
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
        batch_size: int = 1,
    ) -> List[Dict[str, Any]]:
        """Get entity linking prediction.

        Args:
            content (str): The content to process for entity linking.
            entities (Optional[List[Dict[str, Any]]]): A list of entities to link.
            batch_size (int): The size of each batch for processing. Defaults to 1.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the entities with links.
        """
        entities_with_links = []

        if entities:
            entities_with_links = self._process_entities_with_batching(
                content, entities, batch_size
            )
        else:
            entities_with_links = self._process_text_without_entities(content)

        return entities_with_links

    def _process_entities_with_batching(
        self, content: str, entities: List[Dict[str, Any]], batch_size: int
    ) -> List[Dict[str, Any]]:
        """Process entities with batching.

        Args:
            content (str): The content to process.
            entities (List[Dict[str, Any]]): A list of entities to process.
            batch_size (int): The size of each batch.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the entities with links.
        """
        entities_with_links = []
        num_batches = (
            len(entities) + batch_size - 1
        ) // batch_size  # Calculate the number of batches

        for i in range(num_batches):
            batch_entities = entities[i * batch_size : (i + 1) * batch_size]  # noqa
            batch_content = [content] * len(batch_entities)  # Create a batch of content
            (
                batch_unique_entities_list,
                batch_entities_offsets,
                batch_mention_offsets,
                batch_mention_lengths,
            ) = self._generate_batch_offsets(content, batch_entities)

            if not batch_mention_offsets:
                continue  # Skip if all mention_offsets in the batch are empty

            output = self.model.process_disambiguation_batch(
                list_text=batch_content,
                mention_offsets=batch_mention_offsets,
                mention_lengths=batch_mention_lengths,
                entities=batch_entities_offsets,
            )

            entities_with_links.extend(
                self._generate_entities_with_links(
                    batch_entities, batch_unique_entities_list, output
                )
            )

        return entities_with_links

    def _generate_batch_offsets(
        self, content: str, batch_entities: List[Dict[str, Any]]
    ) -> Tuple[List[str], List[List[int]], List[List[int]], List[List[int]]]:
        """Generate batch offsets for entities.

        Args:
            content (str): The content to process.
            batch_entities (List[Dict[str, Any]]): A list of entities in the batch.

        Returns:
            tuple: A tuple containing lists batches.
        """
        batch_mention_offsets = []
        batch_mention_lengths = []
        batch_entities_offsets = []
        batch_unique_entities_list = []

        for entity in batch_entities:
            (
                unique_entities_list,
                entities_offsets,
                mention_offsets,
                mention_lengths,
            ) = self._generate_offsets(text=content, entities=[entity])

            if not mention_offsets:
                continue

            batch_unique_entities_list.extend(unique_entities_list)
            batch_entities_offsets.append(entities_offsets)
            batch_mention_offsets.append(mention_offsets)
            batch_mention_lengths.append(mention_lengths)

        return (
            batch_unique_entities_list,
            batch_entities_offsets,
            batch_mention_offsets,
            batch_mention_lengths,
        )

    def _generate_entities_with_links(
        self,
        batch_entities: List[Dict[str, Any]],
        batch_unique_entities_list: List[str],
        output: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Generate entities with links from batch output.

        Args:
            batch_entities (List[Dict[str, Any]]): A list of entities in the batch.
            batch_unique_entities_list (List[str]): A list of unique entities.
            output (List[Dict[str, Any]]): The output from the model.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the entities with links.
        """
        entities_with_links = []
        output_index = 0

        for entity in batch_entities:
            try:
                if entity["entity_text"] in batch_unique_entities_list:
                    entity_with_link = entity
                    entity_with_link["wiki_link"] = (
                        "https://www.wikidata.org/wiki/"
                        + output[output_index]["entities"][-1]
                    )
                    entities_with_links.append(entity_with_link)
                    output_index += 1
            except KeyError as e:
                raise KeyError(f"KeyError occurred: {e}")
            except IndexError as e:
                raise IndexError(f"IndexError occurred: {e}")
            except Exception as e:
                raise Exception(f"An unexpected error occurred: {e}")

        return entities_with_links

    def _process_text_without_entities(self, content: str) -> List[Dict[str, Any]]:
        """Process text without entities.

        Args:
            content (str): The content to process.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the entities with links.
        """
        entities_with_links = []
        list_texts = [content]
        output = self.model.process_batch(list_text=list_texts)

        try:
            entity_ner_map = dict(zip(output[0]["entities"], output[0]["md_scores"]))
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
