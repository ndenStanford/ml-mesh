"""Model server."""
# isort: skip_file

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)

# Source
from src.settings import get_settings

settings = get_settings()


@pytest.mark.order(5)
def test_model_server_root(test_client, test_model_name):
    """Tests the running ModelServer instance's root endpoint."""
    root_response = test_client.get(f"{test_model_name}/v1/")

    assert root_response.status_code == 200


@pytest.mark.order(6)
def test_model_server_liveness(test_client, test_model_name):
    """Tests the running ModelServer instance's liveness endpoint."""
    liveness_response = test_client.get(f"{test_model_name}/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


@pytest.mark.order(6)
def test_model_server_readiness(test_client, test_model_name):
    """Tests the running ModelServer instance's readiness endpoint."""
    readiness_response = test_client.get(f"/{test_model_name}/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


@pytest.mark.order(8)
def test_model_server_predict(
    test_client, test_model_name, test_payload, test_payload_query_id
):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    test_response = test_client.post(
        f"/{test_model_name}/v1/predict", json=test_payload
    )
    assert test_response.status_code == 200
    assert test_response.json()["data"]["attributes"]["topic"] is not None

    test_response_query_id = test_client.post(
        f"/{test_model_name}/v1/predict", json=test_payload_query_id
    )
    assert test_response_query_id.status_code == 200
    assert test_response_query_id.json()["data"]["attributes"]["topic"] is not None


@pytest.mark.order(9)
def test_model_server_predict_sample_docs(
    test_client, test_model_name, test_payload_sample_docs
):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    test_response = test_client.post(
        f"/{test_model_name}/v1/predict", json=test_payload_sample_docs
    )
    assert test_response.status_code == 200
    assert test_response.json()["data"]["attributes"]["topic"] is not None


@pytest.mark.order(7)
def test_model_server_bio(test_model_name, test_client, test_expected_bio_output):
    """Tests the running ModelServer's bio endpoint.

    Uses the custom data models for validation and the model card from the model
    artifact as ground truth for the regression test element.
    """
    test_response = test_client.get(f"{test_model_name}/v1/bio")

    assert test_response.status_code == 200
    test_actual_bio_output = test_response.json()

    assert test_actual_bio_output == test_expected_bio_output
