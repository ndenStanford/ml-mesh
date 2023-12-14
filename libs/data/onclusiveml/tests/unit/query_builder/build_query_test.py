"""Test."""

# 3rd party libraries
import pytest  # noqa


def test_el(test_el):
    """Test EL API."""
    assert test_el == "https://www.wikidata.org/wiki/Q312"


def test_ner(test_ner):
    """Test NER API."""
    assert test_ner == ["Amazon", "AMZN"]


def test_query_builder(test_query_builder, expected_query_builder):
    """Test query builder."""
    expected_test_el = expected_query_builder["test_el"]
    expected_test_ner = expected_query_builder["test_ner"]
    expected_test_regex = expected_query_builder["test_regex"]

    actual_test_el, actual_test_ner, actual_test_regex = test_query_builder

    assert actual_test_el == expected_test_el
    assert actual_test_ner == expected_test_ner
    assert actual_test_regex == expected_test_regex


def test_scoring(test_scoring):
    """Test scoring."""
    all_scores, texts, embeddings, cluster_labels = test_scoring
    assert all_scores["silhouette"] > 0
    assert all_scores["intra_cluster_similarity"] > 0
    assert all_scores["w_penalization"] > 0
    assert all_scores["homogeneity_score"] > 0
    assert all_scores["relevance_score"] > 0
