"""Mixins."""

# Standard Library
from abc import abstractmethod
from typing import Any, Dict, Optional, Tuple

# Internal libraries
from onclusiveml.llms.typing import LangchainT


class LangchainConvertibleMixin:
    """Mixin for objects that can be converted as langchain object."""

    @abstractmethod
    def as_langchain(
        self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]
    ) -> Optional[LangchainT]:
        """Convert class as langchain object."""
