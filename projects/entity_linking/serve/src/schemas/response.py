"""Request model."""

# Standard Library
from typing import Any, Dict, Optional, Tuple, List

# 3rd party libraries
from pydantic import BaseModel

class Response(BaseModel):
    entities: Optional[List[Dict]]