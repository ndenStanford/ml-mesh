"""Model server test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)

# Source
from src.serve.server_models import (
    BioResponseModel,
    PredictConfiguration,
    PredictInputContentModel,
    PredictionExtractedEntity,
    PredictionOutputContent,
    PredictRequestModel,
    PredictResponseModel,
)


def test_model_server_root(test_client):
    """Tests the running ModelServer instance's root endpoint."""
    root_response = test_client.get("/v1/")
    assert root_response.status_code == 200


def test_model_server_liveness(test_client):
    """Tests the running ModelServer instance's liveness endpoint."""
    liveness_response = test_client.get("/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness(test_client):
    """Tests the running ModelServer instance's readiness endpoint."""
    readiness_response = test_client.get("/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


@pytest.mark.parametrize("test_record_index", [0, 1, 2])
def test_model_server_predict(
    test_model_name,
    test_client,
    test_inputs,
    test_inference_params,
    test_predictions,
    test_record_index,
):
    """Tests the running ModelServer's predict endpoint by making genuine http requests.

    This test uses the custom data models for validation and the test files from the model
    artifact as ground truth for the regression test element.
    """
    input = PredictRequestModel(
        configuration=PredictConfiguration(return_pos=True, language="en"),
        inputs=PredictInputContentModel(content=test_inputs[test_record_index]),
    )

    test_response = test_client.post(
        f"/v1/model/{test_model_name}/predict", json=input.dict()
    )

    assert test_response.status_code == 200
    actual_output = test_response.json()

    expected_output = PredictResponseModel(
        outputs=PredictionOutputContent(
            predicted_content=[
                PredictionExtractedEntity(**i)
                for i in test_predictions[test_record_index]
            ]
        )
    ).dict()

    assert actual_output == expected_output


@pytest.mark.parametrize("test_input", [("Onclusive is great")])
def test_model_server_predict_no_entities(test_model_name, test_client, test_input):
    """Tests the running ModelServer's predict endpoint such that it returns an empty list
    if the no entities are extracted"""

    input = PredictRequestModel(
        configuration=PredictConfiguration(return_pos=True, language="en"),
        inputs=PredictInputContentModel(content=test_input),
    )

    test_response = test_client.post(
        f"/v1/model/{test_model_name}/predict", json=input.dict()
    )

    assert test_response.status_code == 200
    actual_output = test_response.json()
    assert actual_output == PredictResponseModel(outputs=PredictionOutputContent())


def test_model_server_bio(test_model_name, test_client, test_model_card):
    """Tests the running ModelServer's bio endpoint by making genuine http requests.

    This test uses the custom data models for validation and the model card from the model
    artifact as ground truth for the regression test element.
    """
    test_response = test_client.get(f"/v1/model/{test_model_name}/bio")

    assert test_response.status_code == 200
    actual_output = test_response.json()

    expected_output = BioResponseModel(
        model_name=test_model_name, model_card=test_model_card
    ).dict()

    assert actual_output == expected_output
