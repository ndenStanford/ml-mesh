# isort: skip_file
"""Model server test."""

# 3rd party libraries
import pytest
from unittest.mock import patch

# Internal libraries
from onclusiveml.serving.rest.serve import LivenessProbeResponse, ReadinessProbeResponse

# Apply patches before any other imports
patcher_generate = patch("src.settings.generate_crawler_indices")
mock_generate = patcher_generate.start()
mock_generate.return_value = [
    "crawler-4-2024.03",
    "crawler-4-2024.02",
    "crawler-4-2024.01",
    "crawler-4-2023.12",
    "crawler-4-2023.11",
    "crawler",
]

# Source
from src.serve.model import ServedTopicModel
from src.serve.__main__ import get_model_server


@pytest.mark.order(4)
def test_get_model_server():
    """Tests the utility method get_model_server and the attached server."""
    model_server = get_model_server()

    assert isinstance(model_server.model, ServedTopicModel)
    assert not model_server.model.is_ready()


@pytest.mark.order(6)
def test_model_server_liveness(test_client, test_model_name):
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = test_client.get(f"/{test_model_name}/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().model_dump()


@pytest.mark.order(6)
def test_model_server_readiness(test_client, test_model_name):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = test_client.get(f"/{test_model_name}/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().model_dump()
