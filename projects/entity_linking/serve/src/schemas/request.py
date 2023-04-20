"""Request model."""

# Standard Library
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel

# Source
from src.schemas.type_dict import EntityDictInput


class Request(BaseModel):
    content: str
    entities: Optional[List[EntityDictInput]] = None
    lang: str = "en"
