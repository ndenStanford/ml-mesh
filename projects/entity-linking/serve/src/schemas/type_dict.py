"""Entity linking type dict."""

# 3rd party libraries
from typing_extensions import NotRequired, TypedDict


EntityDictInput = TypedDict(
    "EntityDictInput",
    {
        "entity_type": NotRequired[str],
        "entity_text": NotRequired[str],
        "text": NotRequired[str],
        "score": NotRequired[str],
        "sentence_index": NotRequired[int],
    },
)


EntityDictOutput = TypedDict(
    "EntityDictOutput",
    {
        "entity_type": NotRequired[str],
        "entity_text": NotRequired[str],
        "text": NotRequired[str],
        "score": NotRequired[str],
        "sentence_index": NotRequired[int],
        "wiki_link": NotRequired[str],
    },
)
