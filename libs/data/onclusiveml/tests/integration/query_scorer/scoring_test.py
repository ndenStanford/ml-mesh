"""Scoring Test."""

# 3rd party libraries
import pytest  # noqa


def test_scoring(test_scoring):
    """Test scoring."""
    all_scores, texts, embeddings, cluster_labels = test_scoring
    assert all_scores["silhouette"] > 0
    assert all_scores["intra_cluster_similarity"] > 0
    assert all_scores["w_penalization"] > 0
    assert all_scores["homogeneity_score"] > 0
    assert all_scores["relevance_score"] > 0
