"""Entity linking handler."""

# Standard Library
import json
import re
from collections import Counter
from typing import Any, Dict, List, Optional

# 3rd party libraries
import requests

# Internal libraries
# Internal library
from onclusiveml.core.logging import get_default_logger

# Source
from src.schemas import EntityDictInput
from src.settings import settings


logger = get_default_logger(__name__)


def generate_entity_query(text: str, entities: EntityDictInput) -> List[Dict[str, Any]]:
    """Generate a component of query to be consumed by the entity fish endpoint.

    Args:
        text (str): text to be wiki linked
        entities (Optional[EntityDictInput]):
            entities within text recognized by an external NER model
    """
    entity_query = []
    unique_entity_text = set([get_entity_text(entity) for entity in entities])
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


def generate_query(text: str, lang: str, entities: EntityDictInput) -> Dict[str, Any]:
    """Generate the entire query to be consumed by the entity fish endpoint.

    Args:
        text (str): text to be wiki linked
        lang (str): language of the text
        entities (Optional[EntityDictInput]):
            entities within text recognized by an external NER model
    """
    entities_query = generate_entity_query(text, entities)
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
    q = requests.post(url, json=query)
    return q.json()


def get_entity_linking(
    text: str, lang: str = "en", entities: Optional[List[EntityDictInput]] = None
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
        print(entities)

    query = generate_query(text, lang, entities)
    wiki_response = query_wiki(query)
    entity_fish_entities = wiki_response["entities"]

    for entity in entities:
        entity_text = get_entity_text(entity)
        wiki = get_wiki_id(entity_text, entity_fish_entities)  # noqa
        if wiki:
            wiki_link = "https://www.wikidata.org/wiki/{}".format(wiki)
            entity["wiki_link"] = wiki_link

    return entities


def get_entity_text(entity: Dict[str, Any]) -> str:
    """Fetch entity text from entities dictionary"""
    entity_text = entity.get("text")
    if entity_text is None:
        entity_text = entity.get("entity_text")
    return entity_text  # noqa


def get_wiki_id(
    entity_text: str, entity_fish_entities: List[Dict[str, Any]]
) -> Optional[str]:
    """Get most likely Wiki id of a single entity from wiki fish API return

    Args:
        entity_text (str): entity to find corresponding wiki data id
        entity_fish_entities (List[Dict[str, Any]]): Response from entity fish API
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


def entity_text_match(text_1: str, text_2: str) -> bool:
    """Match entity in the tntities dictionary with one from the entity fish API response"""
    if (text_1 in text_2) or (text_2 in text_1):
        return True
    else:
        return False
