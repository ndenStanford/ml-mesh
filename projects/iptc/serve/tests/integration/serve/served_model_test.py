"""Served model test."""

# 3rd party libraries
import pytest

# Source
from src.serve.model import ServedIPTCModel
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings


settings = get_settings()


@pytest.mark.order(1)
def test_served_iptc_model__init__(test_served_model_artifacts):
    """Tests the constructor of the ServedIPTCModel.

    EXCLUDING the loading of genuine model artifacts from local disk.
    """
    ServedIPTCModel(served_model_artifacts=test_served_model_artifacts)


@pytest.mark.order(2)
def test_served_iptc_model_load(test_served_model_artifacts):
    """Tests the constructor of the ServedIPTCModel.

    INCLUDING the loading of genuine model artifacts from local disk.
    """
    served_iptc_model = ServedIPTCModel(
        served_model_artifacts=test_served_model_artifacts
    )

    assert not served_iptc_model.is_ready()

    served_iptc_model.load()

    assert served_iptc_model.is_ready()


@pytest.mark.order(3)
@pytest.mark.parametrize("test_record_index", [0, 1])
def test_served_iptc_model_predict(
    test_served_model_artifacts,
    test_inputs,
    test_inference_params,
    test_predictions,
    test_record_index,
):
    """Tests the fully initialized and loaded ServedIPTCModel's predict method.

    This test uses the custom data models for validation and the test files from
    the model artifact as ground truth for the regression test element.
    """
    served_iptc_model = ServedIPTCModel(
        served_model_artifacts=test_served_model_artifacts
    )
    served_iptc_model.load()

    input = PredictRequestSchema.from_data(
        namespace=settings.model_name,
        attributes={"content": test_inputs[test_record_index]},
        parameters=test_inference_params,
    )

    actual_output = served_iptc_model.predict(input)
    output_data = actual_output.dict()["data"]
    actual_output = PredictResponseSchema.from_data(
        version=actual_output.dict()["version"],
        namespace=output_data["namespace"],
        attributes={"iptc": [output_data["attributes"]["iptc"][0]]},
    )
    expected_output = PredictResponseSchema.from_data(
        version=int(settings.api_version[1:]),
        namespace=settings.model_name,
        attributes={
            "iptc": [
                {
                    "label": test_predictions[test_record_index]["label"],
                    "score": test_predictions[test_record_index]["score"],
                }
            ]
        },
    )

    assert actual_output == expected_output


@pytest.mark.order(3)
def test_served_iptc_model_bio(
    test_model_name, test_served_model_artifacts, test_model_card
):
    """Tests the fully initialized and loaded ServedIPTCModel's bio method.

    This test uses the custom data models for validation and the model card from
    the model artifact as ground truth for the regression test element.
    """
    served_iptc_model = ServedIPTCModel(
        served_model_artifacts=test_served_model_artifacts
    )

    served_iptc_model.load()

    actual_output = served_iptc_model.bio()
    expected_output = BioResponseSchema.from_data(
        version=int(settings.api_version[1:]),
        namespace=settings.model_name,
        attributes={"model_name": test_model_name, "model_card": test_model_card},
    )

    assert actual_output == expected_output
