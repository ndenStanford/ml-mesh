"""Exceptions."""

# Standard Library
from string import Formatter
from typing import Dict, List


class OnclusiveException(Exception):
    """Base Exception class."""

    message_format: str

    def __init__(self, **kwargs) -> None:  # type: ignore
        """Init method."""
        for k in self.kwargs:
            setattr(self, k, kwargs.get(k))

    @property
    def kwargs(self) -> List[str]:
        """Infers kwargs to initialize class from message format."""
        return [
            p for _, p, _, _ in Formatter().parse(self.message_format) if p is not None
        ]

    def _param_dct(self) -> Dict:
        """Message format parameters as a dictionary."""
        return {k: getattr(self, k) for k in self.kwargs}

    @property
    def message(self) -> str:
        """Message builder from message format."""
        return self.message_format.format(**self._param_dct())

    def __str__(self) -> str:
        return self.message
