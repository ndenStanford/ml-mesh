from typing_extensions import TypedDict, NotRequired
from typing import Any, Dict, Optional, Tuple, List

EntityDictInput = TypedDict('EntityDictInput', {'entity_type': NotRequired[str], 'entity_text': NotRequired[str], 'text': NotRequired[str], 
                                                'score': NotRequired[str], 'sentence_index': NotRequired[int]})

EntityDictOutput = TypedDict('EntityDictInput', {'entity_type': NotRequired[str], 'entity_text': NotRequired[str], 'text': NotRequired[str], 
                                                'score': NotRequired[str], 'sentence_index': NotRequired[int], 'wiki_link': NotRequired[str]})