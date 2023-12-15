"""Conftest."""

# 3rd party libraries
import pytest  # noqa

# Internal libraries
from onclusiveml.query_scorer import evaluate_query as query_evaluation
from onclusiveml.query_scorer.settings import get_settings


settings = get_settings()


@pytest.fixture
def evaluate_query_test(build_query_test):
    """Get results."""
    test_el, _, _ = build_query_test
    return test_el, settings.clustering_config, settings.scoring_config


@pytest.fixture
def test_scoring(evaluate_query_test):
    """Test scoring."""
    return query_evaluation(settings.es, settings.es_index, *evaluate_query_test)
