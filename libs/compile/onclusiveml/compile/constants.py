"""Constants."""

# Internal libraries
from onclusiveml.core.base import OnclusiveStrEnum


class CompileWorkflowTasks(OnclusiveStrEnum):
    """Compiled workflow tasks."""

    COMPILE = "compile"
    TEST = "test"
    DOWNLOAD = "download"
    UPLOAD = "upload"
