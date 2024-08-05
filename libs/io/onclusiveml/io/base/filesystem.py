"""Filesystem."""

# Standard Library
import datetime
from abc import abstractclassmethod, abstractmethod
from io import DEFAULT_BUFFER_SIZE
from typing import IO, Any, List, Optional, Set

# Internal libraries
from onclusiveml.core.base import OnclusiveFrozenModel
from onclusiveml.core.base.metaclasses import Context


class FileInfo(OnclusiveFrozenModel):
    """File metadata."""

    size: Optional[int] = None
    created: Optional[datetime.datetime] = None
    last_modified: Optional[datetime.datetime] = None
    path: Optional[str] = None


class BaseFileSystem(metaclass=Context):
    """Abstract FileSystem base class.

    Design inspired by the `Filesystem` abstraction in TFX:
    https://github.com/tensorflow/tfx/blob/master/tfx/dsl/io/filesystem.py
    """

    def __init__(
        self, supported_schemes: Set[str] = set(), root_index: int = 0
    ) -> None:
        """Base contructor."""
        self._supported_schemes = supported_schemes
        self._root_index = root_index

    @property
    def supported_schemes(self) -> Set[str]:
        """Supported schemes."""
        return self._supported_schemes

    @property
    def root_index(self) -> int:
        """Filesystem root index."""
        return self._root_index

    @abstractmethod
    def open(
        self,
        path: "OnclusivePath",
        mode: str = "r",
        buffering: int = DEFAULT_BUFFER_SIZE,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        newline: Optional[str] = None,
    ) -> IO[Any]:
        """Open a file at the given path.

        Args:
            path: The path to the file.
            mode: The mode to open the file.

        Returns:
            Any: The file object.
        """

    @abstractmethod
    def cp(
        self, src: "OnclusivePath", dst: "OnclusivePath", overwrite: bool = False
    ) -> None:
        """Copy a file from the source to the destination.

        Args:
            src: The path of the file to copy.
            dst: The path to copy the source file to.
            overwrite: Whether to overwrite the destination file if it exists.

        Raises:
            FileExistsError: If a file already exists at the destination and
                `overwrite` is not set to `True`.
        """

    @abstractmethod
    def exists(self, path: "OnclusivePath") -> bool:
        """Check whether a given path exists.

        Args:
            path: The path to check.

        Returns:
            `True` if the given path exists, `False` otherwise.
        """

    @abstractmethod
    def glob(self, pattern: "OnclusivePath") -> List["OnclusivePath"]:
        """Find all files matching the given pattern.

        Args:
            pattern: The pattern to match.

        Returns:
            A list of paths matching the pattern.
        """

    @abstractmethod
    def ls(self, path: "OnclusivePath") -> List["OnclusivePath"]:
        """Lists all files in a directory.

        Args:
            path: The path to the directory.

        Returns:
            A list of files in the directory.
        """

    @abstractmethod
    def mkdirs(self, path: "OnclusivePath") -> None:
        """Make a directory at the given path, recursively creating parents.

        Args:
            path: Path to the directory.
        """

    @abstractmethod
    def mkdir(self, path: "OnclusivePath") -> None:
        """Make a directory at the given path; parent directory must exist.

        Args:
            path: Path to the directory.
        """

    @abstractmethod
    def rm(self, path: "OnclusivePath") -> None:
        """Remove the file at the given path. Dangerous operation.

        Args:
            path: The path to the file to remove.

        Raises:
            FileNotFoundError: If the file does not exist.
        """

    @abstractmethod
    def rmtree(self, path: "OnclusivePath") -> None:
        """Deletes a directory recursively. Dangerous operation.

        Args:
            path: The path to the directory to delete.
        """

    @abstractmethod
    def info(self, path: "OnclusivePath") -> List[FileInfo]:
        """Get the info for a given file path.

        Args:
            path: The path to the file.

        Returns:
            The FileInfo object
        """

    @abstractmethod
    def isglob(self, path: "OnclusivePath") -> bool:
        """Check whether the given path is a glob.

        Args:
            path: The path to check.

        Returns:
            `True` if the given path is a glob, `False` otherwise.
        """

    @abstractmethod
    def isfile(self, path: "OnclusivePath") -> bool:
        """Check whether the given path is a file.

        Args:
            path: The path to check.

        Returns:
            `True` if the given path is a file, `False` otherwise.
        """

    @abstractmethod
    def isdir(self, path: "OnclusivePath") -> bool:
        """Check whether the given path is a directory.

        Args:
            path: The path to check.

        Returns:
            `True` if the given path is a directory, `False` otherwise.
        """


class BaseRemoteFileSystem(BaseFileSystem):
    """Base class for remote file systems."""

    @abstractclassmethod
    def from_path(cls, path: "OnclusivePath") -> "BaseRemoteFileSystem":
        """Instanciate remote filesystem from path."""

    @abstractclassmethod
    def upload(cls, source: "OnclusivePath", destination: "OnclusivePath") -> None:
        """Instanciate remote filesystem from path."""

    @abstractclassmethod
    def download(cls, source: "OnclusivePath", destination: "OnclusivePath") -> None:
        """Instanciate remote filesystem from path."""
