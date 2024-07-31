"""Github filesystem."""

# Standard Library
from typing import Any, Callable, ClassVar, Iterable, List, Optional, Set, Tuple

# Internal libraries
from onclusiveml.io.base import BaseFileSystem


class GithubFileSystem(BaseFilesystem):
    """Github filesystem."""

    SUPPORTED_SCHEMES: ClassVar[Set[str]] = {"github://"}
