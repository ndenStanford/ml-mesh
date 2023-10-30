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


# --- atomic settings and models
CLASS_DICT_FIRST = {
    "root": {
        "LABEL_0": "arts, culture, entertainment and media",
        "LABEL_1": "conflict, war and peace",
        "LABEL_2": "crime, law and justice",
        "LABEL_3": "disaster, accident and emergency incident",
        "LABEL_4": "economy, business and finance",
        "LABEL_5": "education",
        "LABEL_6": "environment",
        "LABEL_7": "health",
        "LABEL_8": "labour",
        "LABEL_9": "lifestyle and leisure",
        "LABEL_10": "politics",
        "LABEL_11": "religion",
        "LABEL_12": "science and technology",
        "LABEL_13": "society",
        "LABEL_14": "sport",
        "LABEL_15": "weather",
    }
}


# --- settings classes
class TrackedIPTCModelSpecs(TrackedModelSpecs):
    """Tracked iptc model settings."""

    project: str = "onclusive/iptc"
    model = "IPTC-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class BaseTrackedModelSpecs(TrackedModelSpecs):
    """Trained model settings."""

    project: str = "onclusive/iptc"
    model: str = "IPTC-BASE"
    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = "IPTC-BASE-14"
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
    """IPTCiment settings."""

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class IPTCModelParams(TrackedParams):
    """IPTC Model parameters."""

    huggingface_pipeline_task: str = "text-classification"

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
