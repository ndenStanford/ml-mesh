"""Constants."""

# Internal libraries
from onclusiveml.core.base import OnclusiveEnum


class CeleryStatusTypes(str, OnclusiveEnum):
    """Enum values for celery status types."""

    PENDING: str = "PENDING"
    STARTED: str = "STARTED"
    SUCCESS: str = "SUCCESS"
    FAILURE: str = "FAILURE"


class V3ResponseKeys(str, OnclusiveEnum):
    """Enum values for celery status types."""

    TASK_ID: str = "task_id"
    STATUS: str = "status"
    ERROR: str = "error"
    RESULT: str = "result"
