"""Pathmodule."""

# Standard Library
from abc import ABC, abstractmethod
from typing import List, Tuple, Union


class BasePathModule(ABC):
    """Base class for path modules, which do low-level path manipulation.

    Path modules provide a subset of the os.path API, specifically those
    functions needed to provide PurePathBase functionality. Each PurePathBase
    subclass references its path module via a 'pathmod' class attribute.
    Every method in this base class raises an UnsupportedOperation exception.
    """

    @classmethod
    def _unsupported_msg(cls, attribute):
        return f"{cls.__name__}.{attribute} is unsupported"

    @property
    @abstractmethod
    def sep(self):
        """The character used to separate path components."""

    @property
    @abstractmethod
    def schemesep(self):
        """Scheme separator character."""

    @abstractmethod
    def join(self, path: str, *paths) -> str:
        """Join path segments."""
        """Join path segments."""

    @abstractmethod
    def split(self, path: str) -> Union[Tuple[List[str], str], Tuple[List[str]]]:
        """Splits path.

        Split the path into a pair (head, tail), where *head* is everything
        before the final path separator, and *tail* is everything after.
        Either part may be empty.

        Args:
            path (str): path to splits
        """

    @abstractmethod
    def splitdrive(self, path: str) -> Tuple[str, str]:
        """Split the path into a 2-item tuple (drive, tail).

        The *drive* is a device name or mount point, and *tail* is
        everything after the drive. Either part may be empty.

        Args:
            path (str): string path.
        """

    @abstractmethod
    def normcase(self, path: str) -> str:
        """Normalize the case of the path."""

    @abstractmethod
    def isabs(self, path: str) -> bool:
        """Returns whether the path is absolute.

        Args:
            path (str): string path.
        """
