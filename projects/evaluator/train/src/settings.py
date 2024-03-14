"""Settings."""

# Standard Library
import os
from typing import List

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedParams,
)


# Settings classes
class TrackedDocumentEvaluatorSpecs(TrackedModelSpecs):
    """Params class for specifying the neptune project and model suite."""

    project: str = "onclusive/document-evaluator"
    model: str = "DOCUMENT-EVALUATOR"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class DocumentEvaluatorParams(TrackedParams):
    """Ground truth specification for document evaluator model."""

    # LightGBM parameters
    lgb_params: dict = {"objective": "binary", "verbose": -1, "is_unbalance": True}

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
    config_file_path: str = "config/dev.env"
    # Training settings
    test_size: float = 0.2
    random_state: int = 7
    num_boost_rounds: int = 10000


class TrackedDocumentEvaluatorModelCard(TrackedModelCard):
    """The model card for the document evaluator ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: DocumentEvaluatorParams = DocumentEvaluatorParams()
    # admin
    local_output_dir: str = os.path.join(".", "document_evaluator_artifacts")
    logging_level: str = "INFO"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
