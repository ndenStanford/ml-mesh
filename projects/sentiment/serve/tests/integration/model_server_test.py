# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)

# Source
from src.serve.model_server import get_model_server
from src.served_model import ServedSentModel


@pytest.mark.order(4)
def test_get_model_server():
    """Tests the utility method get_model_server to provide an initialized (but not running)
    ModelServer instance. Also checks that the expected ServedSentModel instance is attached
    and not loaded."""

    model_server = get_model_server()

    assert isinstance(model_server.model, ServedSentModel)
    assert not model_server.model.is_ready()


@pytest.mark.order(5)
def test_model_server_root(test_client):
    """Tests the root endpoint of a ModelServer (not running) instance using starlette's
    TestClient"""

    root_response = test_client.get("/v1/")

    assert root_response.status_code == 200


@pytest.mark.order(6)
def test_model_server_liveness(test_client):
    """Tests the liveness endpoint of a ModelServer (not running) instance using starlette's
    TestClient"""

    liveness_response = test_client.get("/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


@pytest.mark.order(6)
def test_model_server_readiness(test_client):
    """Tests the readiness endpoint of a ModelServer (not running) instance using starlette's
    TestClient"""

    readiness_response = test_client.get("/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()
