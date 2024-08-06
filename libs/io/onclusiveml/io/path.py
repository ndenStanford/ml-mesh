"""Path."""

# Standard Library
import os
import posixpath
from abc import ABC
from typing import Iterable, List, Tuple, Union

# Internal libraries
from onclusiveml.io import constants
from onclusiveml.io.base import BaseFileSystem, BasePathModule
from onclusiveml.io.exceptions import UnknownFileSystemException
from onclusiveml.io.filesystems import LocalFileSystem


class OnclusivePathModule(BasePathModule):
    """Onclusive Path module."""

    @property
    def schemesep(self) -> str:
        """The character used to separate path components."""
        return constants.SCHEME_SEPARATOR

    @property
    def sep(self) -> str:
        """The character used to separate path components."""
        return constants.PATH_SEPARATOR

    @property
    def empty(self) -> str:
        """The character used to separate path components."""
        return constants.EMPTY

    def join(self, path: str, *paths) -> str:
        """Join path segments."""
        return os.path.join(path, *paths)

    def splitscheme(self, path: str) -> Union[Tuple[str, str], Tuple[str]]:
        """Splits scheme."""
        p = os.fspath(path)
        scheme_tail = p.split(self.schemesep, 1)
        if len(scheme_tail) == 1:
            return (p, "")
        scheme, tail = scheme_tail
        return tail, scheme

    def split(self, path: str) -> Union[Tuple[List[str], str], Tuple[List[str]]]:
        """Splits path.

        Split the path into a pair (head, tail), where *head* is everything
        before the final path separator, and *tail* is everything after.
        Either part may be empty.

        Args:
            path (str): path to splits
        """
        tail, scheme = self.splitscheme(path)
        parts = tail.split(self.sep)
        if parts[0] == self.empty and len(parts) > 1:
            parts[0] = self.sep
        if parts[-1] == self.empty:
            parts = parts[:-1]
        return parts, scheme

    # NOTE: not sure if this is needed
    def splitdrive(self, path: str) -> Tuple[str, str]:
        """Split the path into a 2-item tuple (drive, tail).

        The *drive* is a device name or mount point, and *tail* is
        everything after the drive. Either part may be empty.

        Args:
            path (str): string path.
        """
        return posixpath.splitdrive(path)

    def normcase(self, path: str) -> str:
        """Normalize the case of the path."""
        return posixpath.normcase(path)

    def isabs(self, path: str) -> bool:
        """Returns whether the path is absolute.

        Args:
            path (str): string path.
        """
        s = os.fspath(path)
        scheme_tail = s.split(self.schemesep, 1)
        return len(scheme_tail) == 2


class OnclusivePath(ABC):
    """Base class for pure path objects.

    Note:
        This class only handles absolute paths.
        This class *does not* provide several magic methods that are defined in
        its subclass PurePath. They are: __fspath__, __bytes__, __reduce__,
        __hash__, __eq__, __lt__, __le__, __gt__, __ge__. Its initializer and path
        joining methods accept only strings, not os.PathLike objects more broadly.
    """

    __slots__ = (
        # The `_raw_path` slot store a joined string path. This is set in the
        # `__init__()` method.
        "_raw_path",
        # The '_resolving' slot stores a boolean indicating whether the path
        # is being processed by `PathBase.resolve()`. This prevents duplicate
        # work from occurring when `resolve()` calls `stat()` or `readlink()`.
        "_resolving",
        # path scheme
        "_scheme",
        "_parts",
    )

    pathmod = OnclusivePathModule()

    def __init__(self, path, *paths):
        _path = self.pathmod.join(path, *paths) if paths else path
        _parts = self.pathmod.split(_path)
        self._parts, self._scheme = _parts[0], _parts[1] if len(_parts) > 0 else [
            self.pathmod.sep
        ]
        if self._parts == [self.pathmod.sep]:
            self._raw_path = self.pathmod.sep
        else:
            self._raw_path = self.pathmod.join(
                self._parts[0], *(self._parts[1:] if len(self._parts) > 1 else [])
            )
        if not isinstance(self._raw_path, str):
            raise TypeError(
                f"path should be a str, not {type(self._raw_path).__name__!r}"
            )
        self._resolving = False

    @property
    def scheme(self) -> str:
        """Return the scheme portion of this path.

        An absolute path's scheme is the leading few characters.
        Consider a few examples:
        ```python
        assert Path("s3://bucket/foo/bar").scheme == "s3"
        assert Path("file:///tmp/foo/bar").scheme == "file"
        """
        if self._scheme == "":
            return constants.DEFAULT_SCHEME
        return self._scheme

    @property
    def root(self) -> str:
        """The root of the path, if any."""
        return self.pathmod.join(
            self.parts[0], *self.parts[: self.filesystem.root_index]
        )

    @property
    def anchor(self) -> str:
        """The concatenation of the scheme and root, or ''."""
        return self.scheme + self.pathmod.schemesep + self.root

    @property
    def name(self) -> str:
        """The final path component, if any."""
        return self.parts[-1]

    @property
    def suffix(self) -> str:
        """Returns the path suffix.

        The final component's last suffix, if any.
        This includes the leading period. For example: '.txt'
        """
        name = self.name
        i = name.rfind(".")
        if 0 < i < len(name) - 1:
            return name[i:]
        else:
            return ""

    @property
    def filesystem(self) -> "BaseFileSystem":
        """Returns the filesystem."""
        # Infer filesystem from context
        infered_filesystem = filesystem_from_context = BaseFileSystem.get_context(
            raise_if_none=False
        )
        # NOTE: infer filesystem from URL.
        if self.scheme == "file":
            infered_filesystem = LocalFileSystem()

        if filesystem_from_context is not None:
            return filesystem_from_context
        elif infered_filesystem is not None:
            return infered_filesystem
        elif filesystem_from_context is None and infered_filesystem is None:
            raise UnknownFileSystemException()

    @property
    def suffixes(self):
        """A list of the final component's suffixes, if any.

        These include the leading periods. For example: ['.tar', '.gz']
        """
        name = self.name
        if name.endswith("."):
            return []
        name = name.lstrip(".")
        return ["." + suffix for suffix in name.split(".")[1:]]

    @property
    def stem(self):
        """The final path component, minus its last suffix."""
        name = self.name
        i = name.rfind(".")
        if 0 < i < len(name) - 1:
            return name[:i]
        else:
            return name

    @property
    def parts(self):
        """Returns sequence-like access to the path."""
        return self._parts

    @property
    def parent(self):
        """The logical parent of the path."""
        return type(self)(
            self.scheme
            + self.pathmod.schemesep
            + self.pathmod.join(self.parts[0], *self.parts[1:-1])
        )

    @property
    def parents(self):
        """A sequence of this path's logical parents."""
        parents = []
        for i in range(1, len(self.parts)):
            parents.append(self.with_segments(self.pathmod.join("", *self.parts[:i])))
        return tuple(parents)

    def with_segments(self, *pathsegments: Iterable[str]):
        """Create a new path object of the same type by combining the given pathsegments.

        This method is called whenever a derivative path is created.

        Args:
            *pathsegments (Iterable[str]): string path segments
        """
        return type(self)(self.root, *pathsegments)

    def with_name(self, name: str) -> "OnclusivePath":
        """Return a new path with the file name changed."""
        return self.with_segments(*self.pathmod.split(self._raw_path)[0][:-1], name)

    def with_stem(self, stem: str) -> "OnclusivePath":
        """Return a new path with the stem changed."""
        return self.with_name(stem + self.suffix)

    def with_suffix(self, suffix: str) -> "OnclusivePath":
        """Return a new path with the file suffix changed.

        If the path has no suffix, add given suffix.
        If the given suffix is an empty string, remove the suffix from the path.

        Args:
            suffix (str): path suffix
        """
        stem = self.stem
        if not suffix:
            return self.with_name(stem)
        elif not stem:
            raise ValueError(f"{self!r} has an empty name")
        elif suffix.startswith(".") and len(suffix) > 1:
            return self.with_name(stem + suffix)
        else:
            raise ValueError(f"Invalid suffix {suffix!r}")

    def is_relative_to(self, other: Union[str, "OnclusivePath"]):
        """Return True if the path is relative to another path or False."""
        if not isinstance(other, OnclusivePath):
            other = OnclusivePath(other)
        anchor0, parts0 = self.anchor, list(reversed(self.parts))
        anchor1, parts1 = other.anchor, list(reversed(other.parts))
        if anchor0 != anchor1:
            return False
        while parts0 and parts1 and parts0[-1] == parts1[-1]:
            parts0.pop()
            parts1.pop()
        for part in parts1:
            if part and part != ".":
                return False
        return True

    def joinpath(self, *pathsegments: Iterable[str]):
        """Combine this path with one or several arguments.

        Args:
            *pathsegments (Iterable[str]): path segments

        Returns: A new path representing either a subpath
        (if all arguments are relative paths)
        or a totally different path (if one of the arguments is anchored).
        """
        return self.with_segments(self._raw_path, *pathsegments)

    def __truediv__(self, key):
        try:
            return self.with_segments(self._raw_path, key)
        except TypeError:
            return NotImplemented

    @property
    def _pattern_str(self):
        """The path expressed as a string, for use in pattern-matching."""
        return str(self)

    def __str__(self):
        """Return the string representation of the path.

        Suitable for passing to system calls.
        """
        return (
            self.scheme + self.pathmod.schemesep + self.pathmod.join("", self._raw_path)
        )

    def __bytes__(self) -> bytes:
        """Return the bytes representation of the path.

        Note:
            This is only recommended to use under Unix.
        """
        return os.fsencode(f"{self}")

    def __repr__(self) -> str:
        return "{}({!r})".format(self.__class__.__name__, str(self))

    def __fspath__(self) -> str:
        """Compatibilty with os.fspath().

        Example:
            ```python
            import os
            from onclusiveml.io import Path
            path: Path = Path("s3://foo/bar")
            str_path: str = os.fspath(path)
            ```
        """
        return str(self)

    def __eq__(self, other: object) -> bool:
        """Enables equality comparisons, e.g.

        Example:
            ```python
            from onclusiveml.io import OnclusivePath
            OnclusivePath("s3://foo/bar") == OnclusivePath("s3://foo/bar")
            ```
        """
        return (
            isinstance(other, OnclusivePath)
            and self.parts == other.parts
            and self.scheme == other.scheme
        )

    @property
    def glob(self) -> List["OnclusivePath"]:
        """Returns glob."""
        return self.filesystem.glob(self)

    @property
    def isfile(self) -> bool:
        """If path is file."""
        return self.filesystem.isfile(self)

    @property
    def isdir(self) -> bool:
        """If path is a folder."""
        return self.filesystem.isdir(self)

    @property
    def exists(self) -> bool:
        """True if path exists."""
        return self.filesystem.exists(self)

    @classmethod
    def from_relative(cls, relative_path: str) -> "OnclusivePath":
        """Create instance from relative path."""
        return cls(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                relative_path,
            )
        )
