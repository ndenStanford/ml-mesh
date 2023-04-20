"""Request model."""

# Standard Library
from typing import Optional, List

# 3rd party libraries
from pydantic import BaseModel

from src.schemas.type_dict import EntityDictInput

class Request(BaseModel):
    content: str
    entities: Optional[List[EntityDictInput]] = None
    lang: str = 'en'