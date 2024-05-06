"""Mixins."""

# Standard Library
from abc import abstractmethod
from typing import Optional

# Internal libraries
from onclusiveml.llm.typing import LangchainT


class LangchainConvertibleMixin:
    """Mixin for objects that can be converted as langchain object."""

    @abstractmethod
    def as_langchain(self) -> Optional[LangchainT]:
        """Convert class as langchain object."""
