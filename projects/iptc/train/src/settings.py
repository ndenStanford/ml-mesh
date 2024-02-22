"""Settings."""

# Standard Library
import os
from typing import List

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import Field

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedParams,
)


# --- settings classes
class TrackedIPTCModelSpecs(TrackedModelSpecs):
    """Tracked iptc model settings."""

    project: str = "onclusive/iptc-00000000"
    model = "IP00000000-TRAINED"

    class Config:
        env_prefix = "trained_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class BaseTrackedModelSpecs(TrackedModelSpecs):
    """Trained model settings."""

    project: str = "onclusive/iptc-00000000"
    model: str = "IP00000000-BASE"
    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = "IP00000000-BASE-1"
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY)

    class Config:
        env_prefix = "base_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):
    """iptc input parameters."""

    sample_documents: List[str] = [""]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class IPTCSettings(TrackedParams):
    """IPTC settings."""

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class IPTCModelParams(TrackedParams):
    """IPTC Model parameters."""

    huggingface_pipeline_task: str = "text-classification"
    base_model_reference: BaseTrackedModelSpecs = BaseTrackedModelSpecs()
    iptc_settings: IPTCSettings = IPTCSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class TrackedIPTCBaseModelCard(TrackedModelCard):
    """The model card for the base model of the iptc ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: IPTCModelParams = IPTCModelParams()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "iptc_model_artifacts")
    logging_level: str = "INFO"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
