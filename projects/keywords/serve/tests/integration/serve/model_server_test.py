"""Model server test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)
from projects.keywords.serve.src.serve.__main__ import get_model_server

# Source
from src.serve.served_model import ServedKeywordsModel


@pytest.mark.order(4)
def test_get_model_server():
    """Tests the prepped model_server."""
    model_server = get_model_server()

    assert isinstance(model_server.model, ServedKeywordsModel)
    assert not model_server.model.is_ready()


@pytest.mark.order(5)
def test_model_server_root(test_client):
    """Tests the root endpoint of a ModelServer (not running) instance."""
    root_response = test_client.get("/keywords/v1/")

    assert root_response.status_code == 200


@pytest.mark.order(6)
def test_model_server_liveness(test_client):
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = test_client.get("/keywords/v1/live/")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


@pytest.mark.order(6)
def test_model_server_readiness(test_client):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = test_client.get("/keywords/v1/ready/")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


@pytest.mark.order(6)
def test_model_docs(test_client):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    docs_response = test_client.get("/keywords/v1/docs")

    assert docs_response.status_code == 200
