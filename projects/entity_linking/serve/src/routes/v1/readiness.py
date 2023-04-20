"""Entity linking prediction."""

# Standard Library

# 3rd party libraries
# Third party libs
from fastapi import APIRouter, HTTPException, status

# Internal libraries
# Internal libs
from onclusiveml.core.logging import get_default_logger

# Source
from src.predict.entity_fishing import get_entity_linking
from src.schemas import Request, Response

text = "I love living in England."
lang = 'en'
entities = [{"text": "England"}]
result = get_entity_linking(text, lang, entities)

logger = get_default_logger(__name__)
router = APIRouter(
    prefix="/ready",
)

@router.get("", status_code=status.HTTP_200_OK)
@router.get("/", status_code=status.HTTP_200_OK)
async def readycheck():  
    text = "I love living in England."
    lang = 'en'
    entities = [{"text": "England"}]
    result = get_entity_linking(text, lang, entities)
    if result[0].get("text") == 'England' and result[0].get("wiki_link") == 'https://www.wikidata.org/wiki/Q21':
        return "OK"
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API not ready",
        )
    