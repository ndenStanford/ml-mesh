"""S3 filesystem."""

# Standard Library
from typing import Any, Callable, ClassVar, Iterable, List, Optional, Set, Tuple

# Internal libraries
from onclusiveml.io.base import BaseFileSystem


class S3FileSystem(BaseFilesystem):
    """S3 filesystem."""

    SUPPORTED_SCHEMES: ClassVar[Set[str]] = {"s3://"}
