"""Conftest."""

# 3rd party libraries
import pytest
from deepeval.metrics import SummarizationMetric
from fastapi import FastAPI
from fastapi.testclient import TestClient
from utils import retrieve_redshift_dataframe

# Source
from src.serve.model import SummarizationServedModel
from src.serve.server import get_model_server
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture(scope="function")
def summarization_model(settings) -> FastAPI:
    """App fixture."""
    # Source
    return SummarizationServedModel(name=settings.model_name)


@pytest.fixture
def test_client():
    """Test client fixture."""
    model_server = get_model_server()

    return TestClient(model_server)


@pytest.fixture
def test_df_path_enriched():
    """Path to enriched dataframe."""
    return "tests/integration/abstractive_summarization_benchmark_dataset_enriched.csv"


@pytest.fixture
def test_df():
    """Query dataframe from Redshift."""
    df = retrieve_redshift_dataframe()
    return df


@pytest.fixture
def deepeval_settings():
    """Deepeval settings."""
    return {
        "percent_success": 0.5,
        "threshold": 0.5,
        "model": "gpt-4",
        "summarization_compression_ratio": 4,
    }


@pytest.fixture
def metric(deepeval_settings):
    """Deepeval metric."""
    metric = SummarizationMetric(
        threshold=deepeval_settings.threshold,
        model=deepeval_settings.model,
        verbose_mode=True,
    )
    return metric
