"""Model."""

# Standard Library
import re
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
from onclusiveml.serving.rest.serve import ServedModel

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

    @property
    def headers(self) -> Dict[str, str]:
        """Request headers."""
        return {settings.api_key_name: settings.internal_ml_api_key.get_secret_value()}

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Prediction."""
        attributes = payload.data.attributes
        parameters = payload.data.parameters

        content = attributes.content
        entities = getattr(attributes, "entities", None)  # Fetch entities if provided

        content = re.sub("\n+", " ", content)

        output = self._predict(texts=content.split(". "))

        entities = [entry["entities"] for entry in output]
        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"entities": entities},
        )

    @filter_language(supported_languages=list(LanguageIso), raise_if_none=True)
    def _predict(
        self,
        content: str,
        entities: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """Language filtered prediction."""
        return self.model.process_batch(texts=content.split(". "))

    def _generate_query(
        self, content: str, lang: str, entities: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate the entire query to be consumed by the entity fish endpoint.

        Args:
            content (str): text to be wiki linked
            lang (str): language of the text
            entities (Optional[EntityDictInput]):
                entities within text recognized by an external NER model
        """
        entities_query = self._generate_entity_query(content, entities)

        query = {
            "text": content,
            "language": {"lang": lang},
            "mentions": [],
            "entities": entities_query,
            "nbest": False,
            "sentence": False,
        }

        return query

    def _query_wiki(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke entity fish endpoint."""
        q = requests.post(
            settings.entity_fishing_endpoint, json=query, headers=self.headers
        )
        return q.json()

    def _get_entity_linking(
        self,
        content: str,
        lang: str = "en",
        entities: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """Link all entities in text to Wiki data id.

        Args:
            content (str): text to be wiki linked
            lang (str): language of the text
            entities (Optional[List[Dict[str, Any]]]): Optional list of entities.
            If provided, the function will not make a request to get the entities.
        """
        if entities is None:
            response = requests.post(
                settings.entity_recognition_endpoint,
                json={
                    "data": {
                        "identifier": "string",
                        "namespace": "ner",
                        "attributes": {
                            "content": content,
                        },
                        "parameters": {"language": lang},
                    }
                },
            ).json()
            entities = response["data"]["attributes"]["entities"]

        query = self._generate_query(content, lang, entities)
        wiki_response = self._query_wiki(query)
        entity_fish_entities = wiki_response.get("entities", [])
        processed_entities = []
        for entity in entities:
            ent = {}
            entity_text = self._get_entity_text(entity)
            score = self._get_entity_score(entity)
            wiki = self._get_wiki_id(entity_text, entity_fish_entities)

            if wiki:
                wiki_link = "https://www.wikidata.org/wiki/{}".format(wiki)
                entity["wiki_link"] = wiki_link
                ent["wiki_link"] = entity["wiki_link"]
            entity.pop("start", None)
            entity.pop("end", None)

            ent["entity_type"] = entity["entity_type"]
            ent["entity_text"] = entity_text
            if "sentence_indexes" in entity:
                ent["sentence_index"] = entity["sentence_indexes"]
            elif "sentence_index" in entity:
                ent["sentence_index"] = entity["sentence_index"]
            ent["score"] = score

            processed_entities.append(ent)

        return processed_entities

    def _get_wiki_id(self, text: str, entities: List[Dict[str, Any]]) -> Optional[str]:
        """Get most likely Wiki id of a single entity from entity fishing backend response.

        Args:
            text (str): text to be wiki linked
            entities (List[Dict[str, Any]]): Response from entity fishing backend
        """
        wiki_list = []
        for entity in entities:
            if entity.get("offsetStart") is not None:
                if entity_text_match(entity["rawName"], text):
                    wiki_list += [entity.get("wikidataId")]

        if len(wiki_list) > 0:
            counter = Counter(wiki_list)
            most_common_wiki = counter.most_common(1)[0][0]
            return most_common_wiki
        else:
            return None

    def _generate_entity_query(
        self, text: str, entities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate a component of query to be consumed by the entity fish endpoint.

        Args:
            text (str): text to be wiki linked
            entities (List[Dict[str, Any]]):
                entities within text recognized by an external NER model
        """
        entity_query = []
        unique_entity_text = set(
            entity.get("entity_text", entity.get("text")) for entity in entities
        )
        for entity_text in unique_entity_text:
            matched_entities = list(re.finditer(entity_text, text))
            spans = [m.span() for m in matched_entities]
            for span in spans:
                offset_start, offset_end = span
                entity_query += [
                    {
                        "rawName": entity_text,
                        "offsetStart": offset_start,
                        "offsetEnd": offset_end,
                    }
                ]
        return entity_query

    def _get_entity_text(self, entity: Dict[str, Any]) -> str:
        """Fetch entity text from entities dictionary."""
        return entity.get("text", "") or entity.get("entity_text", "")

    def _get_entity_score(self, entity: Dict[str, Any]) -> float:
        """Fetch entity score from entities dictionary."""
        return entity.get("score", 0.0) or entity.get("salience_score", 0.0)
