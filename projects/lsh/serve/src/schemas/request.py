"""Request model."""

# Standard Library
from typing import Optional, Tuple

# 3rd party libraries
from pydantic import BaseModel


class Request(BaseModel):
    """Signature request item.

    Holds the required information to be provided in the payload and their type

    Attributes:
        content (str): Text to generate signature for. An empty string is needed (at least)

        lang (Optional[str]): Text to indicate the language

        shingle_list (Optional[int])

        threshold (Optional[float])

        num_perm (Optional[int]))

        weights (Optional[Tuple[float]])
    """

    content: Optional[str]
    language: Optional[str] = "en"
    shingle_list: Optional[int] = 5
    threshold: Optional[float] = 0.6
    num_perm: Optional[int] = 128
    weights: Optional[Tuple[float, float]] = (0.5, 0.5)
