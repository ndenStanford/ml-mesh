"""Settings."""

# Standard Library
import os
from typing import List

# Internal libraries
from onclusiveml.feature_store import FeatureStoreParams
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackingSettings
)
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
    filter_columns: List[str] = []
    filter_values: List[str] = []
    comparison_operators: List[str] = []
    non_nullable_columns: List[str] = []

class TrackedVEModelSpecs(TrackedModelSettings):
    """Tracked iptc model settings."""

    project: str = "onclusive/visitor-estimation"
    model: str = "VE-TRAINED"

class VEModelParams(TrackingSettings):
    """the training argument for huggingface trainer."""

    epochs: int = 3
    
class TrackedVEBaseModelCard(TrackedModelCard):
    """The model card for the base model of the iptc ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: VEModelParams = VEModelParams()
    # admin
    local_output_dir: str = os.path.join(".", "ve_model_artifacts")
    logging_level: str = "INFO"
