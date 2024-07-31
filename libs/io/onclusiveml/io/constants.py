"""Constants."""

# Standard Library
from typing import Optional

# Internal libraries
from onclusiveml.core.base import OnclusiveEnum


PATH_SEPARATOR: str = "/"
SCHEME_SEPARATOR: str = "://"
EMPTY: str = ""
DEFAULT_ENCODING: str = "bytes"
DEFAULT_SCHEME = "file"


class FileEncoding(str, OnclusiveEnum):
    """File encoding formats."""

    BASE64 = "base64"
    JSON = "json"
    TSV = "tsv"
    CSV = "csv"
    GZIP = "gzip"
    YAML = "yaml"
    PARQUET = "parquet"
    PICKLE = "pickle"


class IOScheme(OnclusiveEnum):
    """Path schemes."""

    FILE = "file"
    GITHUB = "github"
    NEPTUNE = "neptune"
    S3 = "s3"
    EFS = "efs"
    UNSPECIFIED = "unspecified"

    def __str__(self) -> Optional[str]:
        """Scheme string conversion."""
        if self.value == "unspecified":
            return None
        return f"{self.value}{SCHEME_SEPARATOR}"
