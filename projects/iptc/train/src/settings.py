"""Settings."""

# Standard Library
import os
from typing import List

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
    model: str = "IP00000000-TRAINED"

    class Config:
        env_prefix = "trained_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class IPTCModelParams(TrackedParams):
    """the training argument for huggingface trainer."""

    epochs: int = 3
    train_batch_size: int = 32
    eval_batch_size: int = 64
    warmup_steps: int = 500
    model_name: str = "xlm-roberta-base"
    learning_rate: float = 5e-5
    evaluation_strategy: str = "epoch"
    save_strategy: str = "epoch"
    save_steps: int = 5000
    save_total_limit: int = 10
    load_best_model_at_end: bool = True
    early_stopping_patience: int = 1
    report_to: str = "neptune"

    selected_text: str = "content"
    temperature: float = 5
    max_length: int = 128
    test_size: float = 0.2

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
    iptc_label: str = "root"
    filter_columns: List[str] = []
    filter_values: List[str] = []
    comparison_operators: List[str] = []
    non_nullable_columns: List[str] = ["content", "topic_1"]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class TrackedIPTCBaseModelCard(TrackedModelCard):
    """The model card for the base model of the iptc ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: IPTCModelParams = IPTCModelParams()
    # admin
    local_output_dir: str = os.path.join(".", "iptc_model_artifacts")
    logging_level: str = "INFO"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
