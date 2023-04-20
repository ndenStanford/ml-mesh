from typing_extensions import TypedDict

EntityDictInput = TypedDict('EntityDictInput', {'entity_type': str, 'entity_text': str, 'score': str, 'sentence_index': int})
EntityDictOutput = TypedDict('EntityDictInput', {'entity_type': str, 'entity_text': str, 'score': str, 'sentence_index': int, 'wiki_link': str})