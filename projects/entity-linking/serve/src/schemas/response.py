"""Request model."""

# Standard Library
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel

# Source
from src.schemas.type_dict import EntityDictOutput


class Response(BaseModel):
    """Response model."""

    entities: Optional[List[EntityDictOutput]]
