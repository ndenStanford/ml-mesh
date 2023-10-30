"""Helpers."""

# Standard Library
from enum import Enum
from typing import List


class OnclusiveEnum(Enum):
    """Onclusive enum class."""

    @classmethod
    def list(cls, names: bool = False) -> List[str]:
        """List enum values or keys."""
        if not names:
            return [field.value for field in cls]
        else:
            return [field.name for field in cls]
