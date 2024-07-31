"""Local filesystem using Python's built-in modules (`os`, `shutil`, `glob`)."""

# Standard Library
import glob
import os
import shutil
from typing import (
    IO,
    Any,
    Callable,
    ClassVar,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
)

# Internal libraries
from onclusiveml.io.base import BaseFileSystem, FileInfo
from onclusiveml.io.constants import IOScheme


class LocalFileSystem(BaseFileSystem):
    """Filesystem that uses local file operations."""

    def __init__(self) -> None:
        """Base contructor."""
        super().__init__(
            supported_schemes={str(IOScheme.FILE)},
        )

    def open(
        self,
        path: "OnclusivePath",
        mode: str = "r",
        buffering: int = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        newline: Optional[str] = None,
    ) -> IO[Any]:
        """Open a file at the given path.

        Args:
            name: The path to the file.
            mode: The mode to open the file.

        Returns:
            Any: The file object.
        """
        return open(
            path.name, mode=mode, encoding=encoding, errors=errors, newline=newline
        )

    def cp(
        self, src: "OnclusivePath", dst: "OnclusivePath", overwrite: bool = False
    ) -> None:
        """Copy a file from the source to the destination.

        Args:
            src: The source path.
            dst: The destination path.
            overwrite: Whether to overwrite the destination file if it exists.

        Raises:
            FileExistsError: If the destination file exists and overwrite is
                False.
        """
        if not overwrite and os.path.exists(dst):
            raise FileExistsError(
                f"Destination file {str(dst)} already exists and argument "
                f"`overwrite` is false."
            )
        shutil.copyfile(src.name, dst.name)

    def exists(self, path: "OnclusivePath") -> bool:
        """Returns `True` if the given path exists.

        Args:
            path: The path to check.

        Returns:
            bool: Whether the path exists.
        """
        return os.path.exists(path)

    def glob(self, pattern: "OnclusivePath") -> List["OnclusivePath"]:
        """Return the paths that match a glob pattern.

        Args:
            pattern: The glob pattern.

        Returns:
            List["OnclusivePath"]: The paths that match the glob pattern.
        """
        return glob.glob(pattern)  # type: ignore[type-var]

    def isdir(self, path: "OnclusivePath") -> bool:
        """Returns whether the given path points to a directory.

        Args:
            path: The path to check.

        Returns:
            bool: Whether the path points to a directory.
        """
        return os.path.isdir(path)

    def ls(self, path: "OnclusivePath") -> List["OnclusivePath"]:
        """Returns a list of files under a given directory in the filesystem.

        Args:
            path: The path to the directory.

        Returns:
            List["OnclusivePath"]: The list of files under the given directory.
        """
        return os.listdir(path)  # type:ignore[return-value]

    def mkdirs(self, path: "OnclusivePath") -> None:
        """Make a directory at the given path, recursively creating parents.

        Args:
            path: The path to the directory.
        """
        os.makedirs(path, exist_ok=True)

    def mkdir(self, path: "OnclusivePath") -> None:
        """Make a directory at the given path; parent directory must exist.

        Args:
            path: The path to the directory.
        """
        os.mkdir(path)

    def rm(self, path: "OnclusivePath") -> None:
        """Remove the file at the given path. Dangerous operation.

        Args:
            path: The path to the file.
        """
        os.remove(path)

    def rmtree(path: "OnclusivePath") -> None:
        """Deletes dir recursively. Dangerous operation.

        Args:
            path: The path to the directory.
        """
        shutil.rmtree(path)

    def stat(self, path: "OnclusivePath") -> Any:
        """Return the stat descriptor for a given file path.

        Args:
            path: The path to the file.

        Returns:
            Any: The stat descriptor for the file.
        """
        return os.stat(path)

    def size(self, path: "OnclusivePath") -> int:
        """Get the size of a file in bytes.

        Args:
            path: The path to the file.

        Returns:
            The size of the file in bytes.
        """
        return os.path.getsize(path)

    def info(self, path: "OnclusivePath") -> List[FileInfo]:
        """Get the info for a given file path.

        Args:
            path: The path to the file.

        Returns:
            The FileInfo object
        """

    def walk(
        self,
        top: "OnclusivePath",
        topdown: bool = True,
        onerror: Optional[Callable[..., None]] = None,
    ) -> Iterable[Tuple["OnclusivePath", List["OnclusivePath"], List["OnclusivePath"]]]:
        """Return an iterator that walks the contents of the given directory.

        Args:
            top: Path of directory to walk.
            topdown: Whether to walk directories topdown or bottom-up.
            onerror: Callable that gets called if an error occurs.

        Yields:
            An Iterable of Tuples, each of which contain the path of the
            current directory path, a list of directories inside the
            current directory and a list of files inside the current
            directory.
        """
        yield from os.walk(  # type: ignore[type-var, misc]
            top, topdown=topdown, onerror=onerror
        )

    def exists(self, path: "OnclusivePath") -> bool:
        """Check if file exists at given path."""
        if self.isdir(path) or self.isfile(path):
            return os.path.exists(str(path))
        if self.isglob(path):
            return len(self.glob(path)) > 0
        return False

    def isfile(self, path: "OnclusivePath") -> bool:
        """Is this entry file-like?"""
        return os.path.isfile(str(path))

    def isdir(self, path: "OnclusivePath") -> bool:
        """Is this entry directory-like?."""
        return os.path.isdir(str(path))


LocalFileSystem._context_class = LocalFileSystem
BaseFileSystem._context_class = LocalFileSystem
