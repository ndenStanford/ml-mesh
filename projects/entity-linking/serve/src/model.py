"""Model."""

# Standard Library
from typing import Any, Dict, Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.helpers import entity_text_match
from src.schemas import (
    BioResponseModel,
    PredictRequestModel,
    PredictResponseModel,
)
from src.settings import get_settings


settings = get_settings()


class EntityLinkingServedModel(ServedModel):
    """Entity linking model."""

    predict_request_model: Type[BaseModel] = PredictRequestModel
    predict_response_model: Type[BaseModel] = PredictResponseModel
    bio_response_model: Type[BaseModel] = BioResponseModel

    def load(self) -> None:
        """Load model."""
        self.ready = True

    def bio(self) -> BioResponseModel:
        """Model bio."""
        return BioResponseModel(model_name=self.name, model_card=self.model_card)

    @property
    def entities(self) -> Optional[Dict[str, Any]]:
        """Entities to be linked."""
        return self._entities

    @property
    def headers(self) -> Dict[str, str]:
        """Request headers."""
        return {
            settings.API_KEY_NAME: settings.INTERNAL_ML_ENDPOINT_API_KEY.get_secret_value()
        }

    def predict(self, payload: PredictRequestModel) -> PredictResponseModel:
        """Prediction."""
        text = payload.content
        text = re.sub("\n+", " ", text)
        self._entities = payload.entities
        lang = payload.lang
        lang = LanguageIso.from_locale(lang)
        output = self._predict(text, lang)
        self._entities = None
        return {"entities": output}

    @filter_language(
        [
            LanguageIso.EN,
            LanguageIso.FR,
            LanguageIso.DE,
            LanguageIso.ES,
            LanguageIso.IT,
            LanguageIso.AR,
            LanguageIso.ZH,
            LanguageIso.RU,
            LanguageIso.JA,
            LanguageIso.PT,
            LanguageIso.FA,
            LanguageIso.UK,
            LanguageIso.SV,
            LanguageIso.BN,
            LanguageIso.HI,
        ]
    )
    def _predict(self, content: str, language: str) -> Dict[str, Any]:
        """Language filtered prediction."""
        return get_entity_linking(text, lang, self.entities)

    def _generate_query(
        self, text: str, lang: str, entities: EntityDictInput
    ) -> Dict[str, Any]:
        """Generate the entire query to be consumed by the entity fish endpoint.
        Args:
            text (str): text to be wiki linked
            lang (str): language of the text
            entities (Optional[EntityDictInput]):
                entities within text recognized by an external NER model
        """
        entities_query = self._generate_entity_query(text, entities)
        query = {
            "text": text,
            "language": {"lang": lang},
            "mentions": [],
            "entities": entities_query,
        }
        return query

    def query_wiki(query: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke entity fish endpoint."""
        url = settings.ENTITY_FISHING_ENDPOINT
        q = requests.post(url, json=query, headers=self.headers)
        return q.json()

    def _get_entity_linking(
        self,
        text: str,
        lang: str = "en",
        entities: Optional[List[EntityDictInput]] = None,
    ) -> List[Dict[str, Any]]:
        """Link all entities in text to Wiki data id
        Args:
            text (str): text to be wiki linked
            lang (str): language of the text
            entities (Optional[EntityDictInput]):
                entities within text recognized by an external NER model
        """
        # using the NER API to get the result of NER and positions
        if entities is None:
            q = requests.post(
                settings.ENTITY_RECOGNITION_ENDPOINT,
                json={"content": text, "return_pos": True},
            )
            assert q.status_code == 200
            entities = json.loads(q.content.decode("utf-8"))["entities"]

        query = self._generate_query(text, lang, entities)
        wiki_response = self._query_wiki(query)
        entity_fish_entities = wiki_response["entities"]

        for entity in entities:
            entity_text = self._get_entity_text(entity)
            wiki = self._get_wiki_id(entity_text, entity_fish_entities)  # noqa
            if wiki:
                wiki_link = "https://www.wikidata.org/wiki/{}".format(wiki)
                entity["wiki_link"] = wiki_link
        return entities

    def _get_entity_text(self, entity: Dict[str, Any]) -> str:
        """Fetch entity text from entities dictionary"""
        entity_text = entity.get("text")
        if entity_text is None:
            entity_text = entity.get("entity_text")
        return entity_text  # noqa

    def _get_wiki_id(
        self, entity_text: str, entities: List[Dict[str, Any]]
    ) -> Optional[str]:
        """Get most likely Wiki id of a single entity from entity fishing backend response.
        Args:
            entity (str): entity to find corresponding wiki data id
            entities (List[Dict[str, Any]]): Response from entity fishing backend
        """
        wiki_list = []
        for entity in entity_fish_entities:
            if entity.get("offsetStart"):
                if entity_text_match(entity["rawName"], entity_text):
                    wiki_list += [entity.get("wikidataId")]

        if len(wiki_list) > 0:
            counter = Counter(wiki_list)
            most_common_wiki = counter.most_common(1)[0][0]
            return most_common_wiki
        else:
            return None

    def generate_entity_query(
        self, text: str, entities: EntityDictInput
    ) -> List[Dict[str, Any]]:
        """Generate a component of query to be consumed by the entity fish endpoint.
        Args:
            text (str): text to be wiki linked
            entities (Optional[EntityDictInput]):
                entities within text recognized by an external NER model
        """
        entity_query = []
        unique_entity_text = set([self._get_entity_text(entity) for entity in entities])
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
