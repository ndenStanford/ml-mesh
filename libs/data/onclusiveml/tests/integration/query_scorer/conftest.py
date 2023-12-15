"""Conftest."""

# 3rd party libraries
import pytest  # noqa

# Internal libraries
from onclusiveml.query_builder import build_query
from onclusiveml.query_scorer import evaluate_query as query_evaluation
from onclusiveml.query_scorer.settings import get_settings


settings = get_settings()


@pytest.fixture
def query_test():
    """Basic params."""
    company: str = "Apple"
    company_ticker: str = "AAPL"
    keywords: List[str] = ["Iphone"]
    return company, company_ticker, keywords


@pytest.fixture
def evaluate_query_test(query_test):
    """Get results."""
    company, company_ticker, keywords = query_test
    test_el, _, _ = build_query(company, company_ticker, keywords, all_keywords=False)
    return test_el, settings.clustering_config, settings.scoring_config


@pytest.fixture
def test_scoring(evaluate_query_test):
    """Test scoring."""
    return query_evaluation(settings.es, settings.es_index, *evaluate_query_test)
