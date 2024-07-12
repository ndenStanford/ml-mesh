"""Enum."""

# Standard Library
from enum import Enum
from typing import List, Optional, TypeVar


T = TypeVar("T")


class OnclusiveEnum(Enum):
    """Onclusive base enum class."""

    @classmethod
    def members(cls) -> List[Enum]:
        """List enum values."""
        return [field for field in cls]

    @classmethod
    def contains(cls, value: T) -> bool:
        """Checks if a l."""
        return value in cls.members()

    @classmethod
    def names(cls) -> List[str]:
        """List enum values."""
        return [field.name for field in cls]

    @classmethod
    def values(cls) -> List[T]:
        """List enum values."""
        return [field.value for field in cls]

    @classmethod
    def from_value(
        cls, value: T, raises_if_not_found: bool = False
    ) -> Optional["OnclusiveEnum"]:
        """Get enum object from value.

        Args:
            value (T): enum value.
            raises_if_not_found (bool): if set to `True`, an exception is
                raised if the value is not found in the enum class.
        """
        for member in cls:
            if value == member.value:
                return member
        if raises_if_not_found:
            raise ValueError(
                f"The specified value {value} is not in the valid range: "
                f"{cls.values()}"
            )
        return None

    @classmethod
    def from_name(
        cls, name: str, raises_if_not_found: bool = False
    ) -> Optional["OnclusiveEnum"]:
        """Get enum object from name.

        Args:
            name (str): enum name.
            raises_if_not_found (bool): if set to `True`, an exception is
                raised if the value is not found in the enum class.
        """
        for member in cls:
            if name == member.name:
                return member
        if raises_if_not_found:
            raise ValueError(
                f"The specified name {name} is not in the valid range: "
                f"{cls.names()}"
            )
        return None


class OnclusiveStrEnum(str, OnclusiveEnum):
    """Onclusive string enum class.

    This enum class should be used for str.

    Note:
        For int Enums, the class enum.IntEnum is available
            as a python 3.8 built-in class.
    """


class OnclusiveIntEnum(int, OnclusiveEnum):
    """Onclusive integer enum class.

    This enum class should be used for int enum values.
    """
