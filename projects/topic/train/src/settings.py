"""Settings."""

# Standard Library
import os
from typing import List, Tuple

# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackedParams,
)


# --- settings classes
class TrackedTopicModelSpecs(TrackedModelSettings):
    """Params class for specifying the neptune project and model suite."""

    project: str = "onclusive/organic-topic"
    model = "TOPICS-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class TopicModelParams(TrackedParams):
    """Ground truth specification for model inference mode.

    Will be used as ground truth inputs for components downstream of `train` (e.g. `compile` and
    `serve`) during testing
    """

    # SentenceTransformer
    embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"
    # CountVectorizer params
    min_df: float = 0.1
    ngram_range: Tuple[int, int] = (1, 2)
    stop_words_lang: str = "en"
    # HDBSCAN params
    min_cluster_size: int = 10
    hdbscan_metric: str = "euclidean"
    cluster_selection_method: str = "eom"
    prediction_data: bool = True
    # UMAP
    n_neighbors: int = 10
    n_components: int = 90  # make it 150 for prod
    min_dist: float = 0.0
    umap_metric: str = "cosine"
    # MaximalMarginalRelevance
    diversity: float = 0.3
    # BERTopic
    verbose: bool = True
    language: str = "multilingual"
    n_gram_range: Tuple[int, int] = (1, 2)

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class TrackedTopicBaseModelCard(TrackedModelCard):
    """The model card for the base model of the keywords ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: TopicModelParams = TopicModelParams()
    # admin
    local_output_dir: str = os.path.join(".", "topic_model_artifacts")
    logging_level: str = "INFO"

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
    filter_columns: List[str] = []
    filter_values: List[str] = []
    comparison_operators: List[str] = []
    non_nullable_columns: List[str] = ["content"]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
