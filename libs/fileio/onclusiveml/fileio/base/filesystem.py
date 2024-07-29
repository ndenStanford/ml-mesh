"""Filesystem."""

# Standard Library
from abc import ABC, abstractmethod
from typing import Any, Callable, ClassVar, Iterable, List, Optional, Set, Tuple


class BaseFileSystem(ABC):
    """Abstract FileSystem base class.

    Design inspired by the `Filesystem` abstraction in TFX:
    https://github.com/tensorflow/tfx/blob/master/tfx/dsl/io/filesystem.py
    """

    SUPPORTED_SCHEMES: ClassVar[Set[str]]

    @abstractmethod
    def open(name: "OnclusivePath", mode: str = "r") -> Any:
        """Opens a file.

        Args:
            name: The path to the file.
            mode: The mode to open the file in.

        Returns:
            The opened file.
        """

    @abstractmethod
    def cp(src: "OnclusivePath", dst: "OnclusivePath", overwrite: bool = False) -> None:
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
    def exists(path: "OnclusivePath") -> bool:
        """Check whether a given path exists.

        Args:
            path: The path to check.

        Returns:
            `True` if the given path exists, `False` otherwise.
        """

    @abstractmethod
    def glob(pattern: "OnclusivePath") -> List["OnclusivePath"]:
        """Find all files matching the given pattern.

        Args:
            pattern: The pattern to match.

        Returns:
            A list of paths matching the pattern.
        """

    @abstractmethod
    def isdir(path: "OnclusivePath") -> bool:
        """Check whether the given path is a directory.

        Args:
            path: The path to check.

        Returns:
            `True` if the given path is a directory, `False` otherwise.
        """

    @abstractmethod
    def ls(path: "OnclusivePath") -> List["OnclusivePath"]:
        """Lists all files in a directory.

        Args:
            path: The path to the directory.

        Returns:
            A list of files in the directory.
        """

    @abstractmethod
    def mkdirs(path: "OnclusivePath") -> None:
        """Make a directory at the given path, recursively creating parents.

        Args:
            path: Path to the directory.
        """

    @abstractmethod
    def mkdir(path: "OnclusivePath") -> None:
        """Make a directory at the given path; parent directory must exist.

        Args:
            path: Path to the directory.
        """

    @abstractmethod
    def rm(path: "OnclusivePath") -> None:
        """Remove the file at the given path. Dangerous operation.

        Args:
            path: The path to the file to remove.

        Raises:
            FileNotFoundError: If the file does not exist.
        """

    @abstractmethod
    def rmtree(path: "OnclusivePath") -> None:
        """Deletes a directory recursively. Dangerous operation.

        Args:
            path: The path to the directory to delete.
        """

    @abstractmethod
    def stat(path: "OnclusivePath") -> Any:
        """Get the stat descriptor for a given file path.

        Args:
            path: The path to the file.

        Returns:
            The stat descriptor.
        """

    def size(path: "OnclusivePath") -> int:
        """Get the size of a file in bytes.

        To be implemented by subclasses but not abstract for backwards
        compatibility.

        Args:
            path: The path to the file.

        Returns:
            The size of the file in bytes.
        """
        return -1

    @abstractmethod
    def walk(
        top: "OnclusivePath",
        topdown: bool = True,
        onerror: Optional[Callable[..., None]] = None,
    ) -> Iterable[Tuple["OnclusivePath", List["OnclusivePath"], List["OnclusivePath"]]]:
        """Return an iterator that walks the contents of the given directory.

        Args:
            top: The path of directory to walk.
            topdown: Whether to walk directories topdown or bottom-up.
            onerror: Callable that gets called if an error occurs.

        Returns:
            An Iterable of Tuples, each of which contain the path of the current
            directory path, a list of directories inside the current directory
            and a list of files inside the current directory.
        """

    @abstractmethod
    def files(path: "OnclusivePath") -> List[str]:
        """Returns filenames from a Path.

        Args:
            path: The path to the file.

        Returns:
            The stat descriptor.
        """
