"""Entity linking prediction."""

# Standard Library
import re
from typing import Any, Dict

# 3rd party libraries
# Third party libs
from fastapi import APIRouter, status

# Source
from src.predict.entity_fishing import get_entity_linking
from src.schemas import Request, Response


# Internal libs


router = APIRouter(
    prefix="/entity-linking",
)


@router.post("/fish", response_model=Response, status_code=status.HTTP_200_OK)
def entity_fish_wiki(item: Request) -> Dict[str, Any]:
    """Returns wiki id linked to entities of item content.

    Args:
        item (Request): parse request arguments.

    Returns:
        Response: entities with Wiki id attached.
    """
    supported_langs = [
        "en",
        "fr",
        "de",
        "es",
        "it",
        "ar",
        "zh",
        "ru",
        "ja",
        "pt",
        "fa",
        "uk",
        "sv",
        "bn",
        "hi",
    ]
    text = item.content
    text = re.sub("\n+", " ", text)
    entities = item.entities
    lang = item.lang
    if lang == "zh-cn" or lang == "zh-tw":
        lang = "zh"
    if lang not in supported_langs:
        lang = "en"
    output = get_entity_linking(text, lang, entities)
    return {"entities": output}
