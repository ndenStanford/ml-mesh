"""Helpers."""

# Standard Library
from enum import Enum
from typing import Any, Dict, List


class OnclusiveEnum(Enum):
    """Onclusive enum class."""

    @classmethod
    def list(cls, names: bool = False) -> List[str]:
        """List enum values or keys."""
        if not names:
            return [field.value for field in cls]
        else:
            return [field.name for field in cls]

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Return dictionary of enum."""
        return {i.name.lower(): i.value for i in cls}
