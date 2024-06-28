"""Settings."""

# Standard Library
import os
from typing import Dict, List, Optional

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackingSettings,
)


# Settings classes
class TrackedDocumentUncompiledContentScoringSpecs(TrackedModelSettings):
    """Params class for specifying the neptune project and DATA suite."""

    project: str = "onclusive/content-scoring"
    model: str = "SCORING-TRAINED"
    with_id: str = "SCORING-TRAINED-14"


class TrackedDocumentContentScoringSpecs(TrackedModelSettings):
    """Params class for specifying the neptune project and model suite."""

    project: str = "onclusive/content-scoring"
    model: str = "SCORING-TRAINED"


class DocumentContentScoringParams(TrackingSettings):
    """Ground truth specification for document content-scoring model."""

    # LightGBM parameters

    numerical_cols: List[str] = ["pagerank", "reach", "score"]
    categorical_cols: List[str] = [
        "lang",
        "media_type",
        "label",
        "publication",
        "country",
        "is_copyrighted",
        "type_of_summary",
    ]
    # File paths
    data_file_path: str = "data/processed_data.parquet"
    # Training settings
    test_size: float = 0.2
    random_state: int = 7
    # Random Forest parameters
    rf_params: Dict[str, Optional[int]] = {
        "n_estimators": 100,
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "random_state": 42,
    }


class TrackedDocumentContentScoringModelCard(TrackedModelCard):
    """The model card for the document content-scoring ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: DocumentContentScoringParams = DocumentContentScoringParams()
    # admin
    local_output_dir: str = os.path.join(".", "content-scoring_artifacts")
    logging_level: str = "INFO"
