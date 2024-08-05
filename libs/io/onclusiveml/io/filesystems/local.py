"""Local filesystem using Python's built-in modules (`os`, `shutil`, `glob`)."""

# Standard Library
import datetime
import glob
import os
import shutil
from typing import IO, Any, List, Optional

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
            path._raw_path, mode=mode, encoding=encoding, errors=errors, newline=newline
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
        shutil.copytree(src._raw_path, dst._raw_path)

    def glob(self, pattern: "OnclusivePath") -> List["OnclusivePath"]:
        """Return the paths that match a glob pattern.

        Args:
            pattern: The glob pattern.

        Returns:
            List["OnclusivePath"]: The paths that match the glob pattern.
        """
        return [type(pattern)(g) for g in glob.glob(pattern._raw_path)]

    def ls(self, path: "OnclusivePath") -> List["OnclusivePath"]:
        """Returns a list of files under a given directory in the filesystem.

        Args:
            path: The path to the directory.

        Returns:
            List["OnclusivePath"]: The list of files under the given directory.
        """
        if path.isfile:
            return [path]
        return [
            type(path)(os.path.join(path.parent, path.stem, f))
            for f in os.listdir(path._raw_path)
        ]

    def mkdirs(self, path: "OnclusivePath") -> None:
        """Make a directory at the given path, recursively creating parents.

        Args:
            path: The path to the directory.
        """
        return os.makedirs(path._raw_path, exist_ok=True)

    def mkdir(self, path: "OnclusivePath") -> None:
        """Make a directory at the given path; parent directory must exist.

        Args:
            path: The path to the directory.
        """
        os.mkdir(path._raw_path)

    def rm(self, path: "OnclusivePath") -> None:
        """Remove the file at the given path. Dangerous operation.

        Args:
            path: The path to the file.
        """
        if self.isfile(path):
            return os.remove(path._raw_path)
        if self.isdir(path):
            return shutil.rmtree(path._raw_path)

    def info(self, path: "OnclusivePath") -> Optional[FileInfo]:
        """Get the info for a given file path.

        Args:
            path: The path to the file.

        Returns:
            The FileInfo object
        """
        if not self.isfile(path):
            return

        stat = os.stat(path._raw_path)

        return FileInfo(
            size=stat.st_size,
            created=datetime.datetime.fromtimestamp(stat.st_ctime),
            last_modified=datetime.datetime.fromtimestamp(stat.st_mtime),
            path=path._raw_path,
        )

    def exists(self, path: "OnclusivePath") -> bool:
        """Check if file exists at given path."""
        if self.isglob(path):
            return len(self.glob(path)) > 0
        return os.path.exists(path._raw_path)

    def isfile(self, path: "OnclusivePath") -> bool:
        """Is this entry file-like?"""
        return os.path.isfile(path._raw_path)

    def isdir(self, path: "OnclusivePath") -> bool:
        """Returns whether the given path points to a directory.

        Args:
            path: The path to check.

        Returns:
            bool: Whether the path points to a directory.
        """
        return os.path.isdir(path._raw_path)

    def isglob(self, path: "OnclusivePath") -> bool:
        """Check whether the given path is a glob.

        Args:
            path: The path to check.

        Returns:
            `True` if the given path is a glob, `False` otherwise.
        """
        return "*" in path._raw_path


LocalFileSystem._context_class = LocalFileSystem
BaseFileSystem._context_class = LocalFileSystem
