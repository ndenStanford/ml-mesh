"""Request model."""

# Standard Library
from typing import Optional

# 3rd party libraries
from pydantic import BaseModel

class Request(BaseModel):
    content: str
    entities: Optional[list] = None
    lang: str = 'en'