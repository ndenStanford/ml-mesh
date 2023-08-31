"""Helpers."""

# Standard Library
from enum import Enum
from typing import List


class OnclusiveEnum(Enum):
    """Onclusive enum class."""

    @classmethod
    def list(cls) -> List[str]:
        """List enum values."""
        return [field.value for field in cls]
