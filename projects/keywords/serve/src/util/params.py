"""Settings."""

# 3rd party libraries
from neptune.types.mode import Mode

# Internal libraries
from onclusiveml.tracking import TrackedModelSettings


class TrackedCompiledModelSpecs(TrackedModelSettings):
    """Tracked model specs."""

    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str
    # we only need to download from the base model, not upload
    mode: str = Mode.READ_ONLY
