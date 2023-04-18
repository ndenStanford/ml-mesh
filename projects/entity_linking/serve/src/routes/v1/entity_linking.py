"""Entity linking prediction."""

# Standard lib

# Standard Library
from typing import Dict, Optional

# 3rd party libraries
# Third party libs
from fastapi import APIRouter, status

# Internal libraries
# Internal libs
from onclusiveml.core.logging import get_default_logger

# Source
from src.predict.summarization import handle
from src.schemas import Request, Response


logger = get_default_logger(__name__)

router = APIRouter(
    prefix="/entity-linking",
)

@router.post("/fish", response_model=Response, status_code=status.HTTP_200_OK)
def entity_fish_wiki(item: Item): # item is an instance of Item class
    supported_langs = ["en", "fr", "de", "es", "it", "ar","zh","ru","ja","pt","fa","uk","sv", "bn","hi"]
    text = item.content
    text = re.sub('\n+',' ', text)
    entities = item.entities
    lang = item.lang
    if lang == "zh-cn" or lang == "zh-tw":
        lang = "zh"
    if lang not in supported_langs:
        lang = "en"
    output = get_entity_linking(text, lang, entities)
    return {'entities': output}