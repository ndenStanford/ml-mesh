"""Settings."""

# Standard Library
import os
from typing import List

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import Field

# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams
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

    sample_documents: List[str] = [
        "Stocks reversed earlier losses to close higher despite rising oil prices that followed \
        the attack by Hamas on Israel over the weekend. Dovish comments by \
        Federal Reserve officials boosted the three major indexes. \
        The Dow Jones Industrial Average added nearly 200 points.",
        "Art is a diverse range of human activity, and resulting product,\
        that involves creative or imaginative talent expressive of technical \
        proficiency, beauty, emotional power, or conceptual ideas",
    ]

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

    """the training argument for huggingface trainer"""
    epochs: int = 3
    train_batch_size: int = 32
    eval_batch_size: int = 64
    warmup_steps: int = 500
    model_name: "xlm-roberta-base"
    learning_rate: str = "5e-5"
    save_steps: int = 5000
    save_total_limit: int = 10
    early_stopping_patience: int = 1
    report_to: str = "neptune"

    level: int = 1
    first_level_root_id: int
    second_level_root_id: int
    selected_text: str = "content"
    temperature: float = 5

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class DataFetchParams(FeatureStoreParams):
    """Feature registration inputs."""

    entity_name: str
    entity_join_key: str
    feature_view_name: str
    dataset_upload_bucket: str
    dataset_upload_dir: str
    save_artifact: bool = False
    n_records_sample: int
    n_records_full: int

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
