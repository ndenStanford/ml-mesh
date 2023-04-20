from typing_extensions import TypedDict, NotRequired

EntityDictInput = TypedDict('EntityDictInput', {'entity_type': NotRequired[str], 'entity_text': NotRequired[str], 'text': NotRequired[str], 
                                                'score': NotRequired[str], 'sentence_index': NotRequired[int]})

EntityDictOutput = TypedDict('EntityDictInput', {'entity_type': NotRequired[str], 'entity_text': NotRequired[str], 'text': NotRequired[str], 
                                                'score': NotRequired[str], 'sentence_index': NotRequired[int], 'wiki_link': NotRequired[str]})