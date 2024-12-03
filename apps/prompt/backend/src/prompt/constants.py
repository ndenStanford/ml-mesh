"""Constants."""

# Internal libraries
from onclusiveml.core.base import OnclusiveEnum


class CeleryStatusTypes(str, OnclusiveEnum):
    """Enum values for celery status types."""

    PENDING: str = "PENDING"
    STARTED: str = "STARTED"
    SUCCESS: str = "SUCCESS"
    FAILURE: str = "FAILURE"


GENERATED: str = "generated"
