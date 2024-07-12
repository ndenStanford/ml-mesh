"""Constants."""

# Internal libraries
from onclusiveml.core.base import OnclusiveStrEnum


class ModelType(OnclusiveStrEnum):
    """Model types."""

    BASE = "base"
    TRAINED = "trained"
    COMPILED = "compiled"
