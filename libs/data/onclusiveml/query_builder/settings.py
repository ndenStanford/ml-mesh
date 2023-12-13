"""Settings."""

# Standard Library
import os
from typing import Any, List

# 3rd party libraries
from elasticsearch import Elasticsearch
from pydantic import BaseModel, HttpUrl, SecretStr


class ClusteringConfig(BaseModel):
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


class ScoringConfig(BaseModel):
    """ScoringConfig."""

    w_silhouette: float = 0.5
    w_intra_cluster: float = 0.5
    w_relevance: float = 0.5
    w_homogeneity: float = 0.5
    penalty_option: str = "proportion"
    penalty_scaling_power: float = 0.5


class ApiCred(BaseModel):
    """EL."""

    api_key: SecretStr
    url: HttpUrl


class Settings(BaseModel):
    """Settings."""

    es: Any
    clustering_config: ClusteringConfig
    scoring_config: ScoringConfig
    entity_linking_prod: ApiCred
    entity_linking_stage: ApiCred
    NER_prod: ApiCred
    NER_stage: ApiCred
    es_index: List[str]


def get_settings() -> Settings:
    """Get the settings."""
    es = Elasticsearch(
        [
            "https://crawler-prod:GnVjrB5jXgGGzPZHWNRpwWGu4NqTWJsw@search5-client.airpr.com"
        ],
        timeout=30,
        max_retries=10,
        retry_on_timeout=True,
    )

    clustering_config = ClusteringConfig()
    scoring_config = ScoringConfig()

    entity_linking_prod = ApiCred(
        api_key=os.getenv("INTERNAL_ML_PROD_API_KEY"),
        url="https://internal.api.ml.prod.onclusive.com/entity-linking/v1/predict",
    )

    entity_linking_stage = ApiCred(
        api_key=os.getenv("INTERNAL_ML_STAGE_API_KEY"),
        url="https://internal.api.ml.stage.onclusive.com/entity-linking/v1/predict",
    )

    NER_prod = ApiCred(
        api_key=os.getenv("INTERNAL_ML_PROD_API_KEY"),
        url="https://internal.api.ml.prod.onclusive.com/ner/v1/predict",
    )

    NER_stage = ApiCred(
        api_key=os.getenv("INTERNAL_ML_STAGE_API_KEY"),
        url="https://internal.api.ml.stage.onclusive.com/ner/v1/predict",
    )

    es_index = ["crawler", "crawler-2023.11", "crawler-2023.10", "crawler-2023.09"]

    return Settings(
        es=es,
        es_index=es_index,
        clustering_config=clustering_config,
        scoring_config=scoring_config,
        entity_linking_prod=entity_linking_prod,
        entity_linking_stage=entity_linking_stage,
        NER_prod=NER_prod,
        NER_stage=NER_stage,
    )
