# Standard Library
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel


class Response(BaseModel):
    """Signature response item.

    Holds the information on expected output at inference

    Attributes:
        signature (Optional[str]): Signature text in string, can be None
    """

    signature: Optional[List[str]]
