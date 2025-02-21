"""Model server tests."""

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
    PredictInputDocumentModel,
    PredictionExtractedKeyword,
    PredictionOutputDocument,
    PredictRequestModel,
    PredictResponseModel,
)


@pytest.mark.order(6)
def test_model_server_liveness(test_client):
    """Tests the running ModelServer instance's liveness endpoint."""
    liveness_response = test_client.get("/keywords/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().model_dump()


@pytest.mark.order(6)
def test_model_server_readiness(test_client):
    """Tests the running ModelServer instance's readiness endpoint."""
    readiness_response = test_client.get("/keywords/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().model_dump()


@pytest.mark.order(7)
@pytest.mark.parametrize("test_record_index", [0, 1, 2])
def test_model_server_predict(
    test_client,
    test_inputs,
    test_inference_params,
    test_predictions,
    test_record_index,
):
    """Tests the running ModelServer's predict endpoint by making genuine http requests.

    Uses the custom data models for validation and the test files from the model artifact
    as ground truth for the regression test element.
    """
    input = PredictRequestModel(
        configuration=PredictConfiguration(**test_inference_params),
        inputs=[PredictInputDocumentModel(document=test_inputs[test_record_index])],
    )
    test_response = test_client.post("/keywords/v1/predict", json=input.model_dump())

    assert test_response.status_code == 200
    actual_output = test_response.json()

    expected_output = PredictResponseModel(
        outputs=[
            PredictionOutputDocument(
                predicted_document=[
                    PredictionExtractedKeyword(keyword_token=kt, keyword_score=ks)
                    for kt, ks in test_predictions[test_record_index]
                ]
            )
        ]
    ).model_dump()

    assert actual_output == expected_output


@pytest.mark.order(7)
def test_model_server_bio(test_model_name, test_client, test_model_card):
    """Tests the running ModelServer's bio endpoint by making genuine http requests.

    Uses the custom data models for validation and the model card from the model artifact
    as ground truth for the regression test element.
    """
    test_response = test_client.get("/keywords/v1/bio")

    assert test_response.status_code == 200
    actual_output = test_response.json()

    expected_output = BioResponseModel(
        model_name=test_model_name, model_card=test_model_card
    ).model_dump()

    assert actual_output == expected_output
