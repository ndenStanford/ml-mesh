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
from src.serve.server_models import (
    PredictConfiguration,
    PredictInputDocumentModel,
    PredictRequestModel,
)


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


@pytest.mark.order(7)
def test_model_server_predict(
    test_model_name,
    test_client,
    test_predict_input,
    test_expected_predict_output,
):
    """Tests the running ModelServer's predict endpoint.

    Uses the custom data models for validation and the test files from the model
    artifact as ground truth for the regression test element.
    """
    input = PredictRequestModel(
        configuration=PredictConfiguration(),
        inputs=PredictInputDocumentModel(
            industry=test_predict_input.industry,
            content=test_predict_input.content,
        ),
    )

    test_response = test_client.post(
        f"/{test_model_name}/v1/predict", json=input.dict()
    )

    assert test_response.status_code == 200
    test_actual_predict_output = test_response.json()

    assert type(test_actual_predict_output) == dict


@pytest.mark.order(7)
def test_model_server_bio(test_model_name, test_client, test_expected_bio_output):
    """Tests the running ModelServer's bio endpoint.

    Uses the custom data models for validation and the model card from the model
    artifact as ground truth for the regression test element.
    """
    test_response = test_client.get(f"{test_model_name}/v1/bio")

    assert test_response.status_code == 200
    test_actual_bio_output = test_response.json()

    assert test_actual_bio_output
