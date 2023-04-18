"""ntity linking handler."""

# Standard Library
import datetime
import re
from typing import Any, Dict, Optional, Tuple

# 3rd party libraries
# OpenAI library
import openai

# Internal libraries
# Internal library
from onclusiveml.core.logging import 

from src.settings import settings

def generate_query(text, lang, entities):
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

def query_wiki(query):
    url =  settings.ENTITY_FISHING_ENDPOINT
    # url =  'https://eks-data-dev-2.onclusive.com/service/disambiguate'
    q = requests.post(url, json = query)
    return q.json()

def get_entity_linking(text, lang = 'en', entities = None):
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

def get_entity_text(entity):
    entity_text = entity.get('text')
    if entity_text is None:
        entity_text = entity.get('entity_text')
    return entity_text

def get_wiki_id(entity_text, entity_fish_entities):
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

def entity_text_match(text_1, text_2):
    if (text_1 in text_2) or (text_2 in text_1):
        return True
    else:
        return False