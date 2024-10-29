"""Settings."""

# Standard Library
import os
from typing import List, Tuple

# Internal libraries
from onclusiveml.feature_store.settings import FeastFeatureStoreSettings
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackingSettings,
)


# --- settings classes
class TrackedTopicModelSpecs(TrackedModelSettings):
    """Params class for specifying the neptune project and model suite."""

    project: str = "onclusive/organic-topic"
    model: str = "TOPICS-TRAINED"


class TopicModelParams(TrackingSettings):
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


class TrackedTopicBaseModelCard(TrackedModelCard):
    """The model card for the base model of the keywords ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: TopicModelParams = TopicModelParams()
    # admin
    local_output_dir: str = os.path.join(".", "topic_model_artifacts")
    logging_level: str = "INFO"


class DataFetchParams(FeastFeatureStoreSettings):
    """Feature registration inputs."""

    dataset_upload_bucket: str
    dataset_upload_dir: str
    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str
    entity_df: str = ""
    features: List[str] = []
    redshift_timestamp_field: str
    save_artifact: bool = True
    n_records_sample: int
    n_records_full: int
    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str
