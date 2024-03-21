"""Scoring Test."""

# 3rd party libraries
import pytest  # noqa

# Internal libraries
from onclusiveml.data.query_scorer import evaluate_query
from onclusiveml.data.query_scorer.settings import get_settings


settings = get_settings()


def test_scoring(evaluate_query_test):
    """Test scoring."""
    all_scores, texts, embeddings, cluster_labels = evaluate_query(
        settings.es, settings.es_index, *evaluate_query_test
    )
    assert (all_scores["silhouette"] is None) or (all_scores["silhouette"] > 0)
    assert all_scores["intra_cluster_similarity"] > 0
    assert all_scores["w_penalization"] > 0
    assert all_scores["homogeneity_score"] > 0
    assert all_scores["relevance_score"] > 0
