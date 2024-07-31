"""Neptune filesystem."""

# Standard Library
from typing import Any, Callable, ClassVar, Iterable, List, Optional, Set, Tuple

# Internal libraries
from onclusiveml.io.base import BaseFileSystem


class NeptuneFileSystem(BaseFilesystem):
    """Filesystem that uses local file operations."""

    SUPPORTED_SCHEMES: ClassVar[Set[str]] = {"neptune://"}
