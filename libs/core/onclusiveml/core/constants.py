"""Constants."""

# Internal libraries
from onclusiveml.core.base import OnclusiveStrEnum


class Runtime(OnclusiveStrEnum):
    """Enum for runtime types."""

    GITHUB_ACTION = "github_action"
    KUBERNETES = "kubernetes"
    NATIVE = "native"
    NOTEBOOK = "notebook"
    WSL = "wls"


class Environment(OnclusiveStrEnum):
    """Environment types."""

    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"
    UNDEFINED = "undefined"


class OperatingSystem(OnclusiveStrEnum):
    """Enum for OS types."""

    LINUX = "Linux"
    WINDOWS = "Windows"
    MACOS = "Darwin"
