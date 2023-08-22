# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import Field

# Internal libraries
from onclusiveml.tracking import TrackedModelSpecs


class TrackedCompiledModelSpecs(TrackedModelSpecs):
    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = Field("NER-COMPILED-12", env="neptune_model_version_id")
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY, env="neptune_client_mode")
