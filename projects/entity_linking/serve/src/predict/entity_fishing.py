"""Entity linking handler."""

# Standard Library
from typing import Any, Dict, Optional
import requests
from collections import Counter

# Internal libraries
# Internal library
from onclusiveml.core.logging import get_default_logger
from src.schemas import EntityDictInput

from src.settings import settings

logger = get_default_logger(__name__)

def generate_query(text: str, lang: str, entities: EntityDictInput) -> Dict[str, Any]:
    entities_query = [{"rawName": get_entity_text(entity)} for entity in entities]
    query = {
        "text": text,
        "language": {
            "lang": lang
        },
        "mentions": ["ner","wikipedia"],
        "entities": entities_query
    }
    return query

def query_wiki(query: Dict[str, Any])-> Dict[str, Any]:
    url =  settings.ENTITY_FISHING_ENDPOINT
    q = requests.post(url, json = query)
    return q.json()

def get_entity_linking(text: str, lang: str = 'en', entities: EntityDictInput) -> Dict[str, Any]:
    #using the NER API to get the result of NER and positions
    if entities is None:
        q = requests.post(settings.ENTITY_RECOGNITION_ENDPOINT, json = {"content": text, "return_pos": True})
        assert q.status_code == 200
        entities = json.loads(q.content.decode('utf-8'))['entities']
        print(entities)

    query = generate_query(text, lang, entities)
    wiki_response = query_wiki(query)
    entity_fish_entities = wiki_response['entities']

    for entity in entities:
        entity_text = get_entity_text(entity)
        wiki = get_wiki_id(entity_text, entity_fish_entities)
        if wiki:
            wiki_link = 'https://www.wikidata.org/wiki/{}'.format(wiki)
            entity['wiki_link'] = wiki_link
            
    return entities

def get_entity_text(entity: Dict[str, Any]) -> str:
    entity_text = entity.get('text')
    if entity_text is None:
        entity_text = entity.get('entity_text')
    return entity_text

def get_wiki_id(entity_text: str, entity_fish_entities: Dict[str, Any]) -> Optional[str]:
    wiki_list = []
    for entity in entity_fish_entities:
        if entity.get('offsetStart'):
            if entity_text_match(entity['rawName'], entity_text):
                wiki_list += [entity.get('wikidataId')]

    if len(wiki_list) > 0:
        counter = Counter(wiki_list)
        most_common_wiki = counter.most_common(1)[0][0]
        return most_common_wiki
    else:
        return None

def entity_text_match(text_1: str, text_2: str) -> bool:
    if (text_1 in text_2) or (text_2 in text_1):
        return True
    else:
        return False