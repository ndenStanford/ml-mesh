"""Settings."""

# Standard Library
import os
from typing import Any, List

# 3rd party libraries
from elasticsearch import Elasticsearch

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings


class ClusteringConfig(OnclusiveBaseSettings):
    """ClusteringConfig."""

    embedding_method: str = "pretrained"
    model_path: str = "xlm-roberta-base"
    tfidf_max_features: int = 4000
    dimension_reduction_method: str = "tumap'"
    n_components: int = 20
    hdbscan_cluster_selection_method: str = "eom"
    gen_min_span_tree: bool = True
    hdbscan_algorithm: str = "best"
    hdbscan_metric: str = "euclidean"
    hdbscan_min_cluster_size: int = 15
    hdbscan_allow_single_cluster: bool = True
    umap_min_dist: float = 0.1
    umap_n_neighbors: int = 15


class ScoringConfig(OnclusiveBaseSettings):
    """ScoringConfig."""

    w_silhouette: float = 0.5
    w_intra_cluster: float = 0.5
    w_relevance: float = 0.5
    w_homogeneity: float = 0.5
    penalty_option: str = "proportion"
    penalty_scaling_power: float = 0.5


class Elasticsearchconfig(OnclusiveBaseSettings):
    """Elasticsearchconfig."""

    es_url: str = os.getenv("ELASTICSEARCH_URL")


class Settings(OnclusiveBaseSettings):
    """Settings."""

    es: Any
    es_index: List[str]
    clustering_config: ClusteringConfig
    scoring_config: ScoringConfig


def get_settings() -> Settings:
    """Get the settings."""
    elasticsearch_config = Elasticsearchconfig()

    es = Elasticsearch(
        [elasticsearch_config.es_url],
        timeout=30,
        max_retries=10,
        retry_on_timeout=True,
    )

    clustering_config = ClusteringConfig()
    scoring_config = ScoringConfig()

    es_index = ["crawler", "crawler-2023.11", "crawler-2023.10", "crawler-2023.09"]

    return Settings(
        es=es,
        es_index=es_index,
        clustering_config=clustering_config,
        scoring_config=scoring_config,
    )
