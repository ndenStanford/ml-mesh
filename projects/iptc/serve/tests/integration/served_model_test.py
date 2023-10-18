"""Served model test."""

# ML libs
import torch

# 3rd party libraries
import pytest

# Source
from src.serve.served_model import ServedIPTCModel
from src.serve.server_models import (
    BioResponseModel,
    PredictConfiguration,
    PredictInputContentModel,
    PredictionOutputContent,
    PredictRequestModel,
    PredictResponseModel,
)


@pytest.mark.order(1)
def test_served_iptc_model__init__(test_served_model_artifacts):
    """Tests the constructor of the ServedIPTCModel."""
    ServedIPTCModel(served_model_artifacts=test_served_model_artifacts)


@pytest.mark.order(2)
def test_served_iptc_model_load(test_served_model_artifacts):
    """Tests the constructor of the ServedIPTCModel."""
    served_iptc_model = ServedIPTCModel(
        served_model_artifacts=test_served_model_artifacts
    )

    assert not served_iptc_model.is_ready()

    served_iptc_model.load()

    assert served_iptc_model.is_ready()


@pytest.mark.parametrize("test_record_index", [0, 1])
def test_served_iptc_model_predict(
    test_served_model_artifacts,
    test_inputs,
    test_predictions,
    test_record_index,
    test_atol,
    test_rtol,
):
    """Tests the fully initialized and loaded ServedIPTCModel's predict method."""
    served_iptc_model = ServedIPTCModel(
        served_model_artifacts=test_served_model_artifacts
    )
    served_iptc_model.load()
    input = PredictRequestModel(
        configuration=PredictConfiguration(),
        inputs=PredictInputContentModel(content=test_inputs[test_record_index]),
    )

    actual_output = served_iptc_model.predict(input)

    expected_output = PredictResponseModel(
        outputs=PredictionOutputContent(
            predicted_content=[
                {
                    "label": test_predictions[test_record_index].get("label"),
                    "score": test_predictions[test_record_index].get("score"),
                }
            ]
        )
    )

    assert actual_output.outputs[0].label == expected_output.outputs.label
    torch.testing.assert_close(
        actual_output.outputs[0].score,
        expected_output.outputs.score,
        atol=test_atol,
        rtol=test_rtol,
    )


@pytest.mark.parametrize(
    "test_sample_content, test_sample_response",
    [
        (
            """Stocks reversed earlier losses to close higher despite rising oil prices
            that followed the attack by Hamas on Israel over the weekend. Dovish comments by
            Federal Reserve officials boosted the three major indexes. The Dow Jones Industrial
            Average added nearly 200 points.""",
            {"label": "economy, business and finance", "score": 0.9870237112045288},
        )
    ],
)
def test_served_iptc_model_with_iptc_predict(
    test_served_model_artifacts,
    test_sample_content,
    test_sample_response,
    test_predictions,
):
    """Tests the fully initialized and loaded ServedIPTCModel's predict method."""
    served_iptc_model = ServedIPTCModel(
        served_model_artifacts=test_served_model_artifacts
    )
    served_iptc_model.load()
    input = PredictRequestModel(
        configuration=PredictConfiguration(
            # language="en"
        ),
        inputs=PredictInputContentModel(content=test_sample_content),
    )

    actual_output = served_iptc_model.predict(input)

    expected_output = PredictResponseModel(
        outputs=PredictionOutputContent(
            predicted_content=[
                {
                    "label": test_predictions[test_record_index].get("label"),
                    "score": test_predictions[test_record_index].get("score"),
                }
            ]
        )
    )

    assert actual_output.outputs[0].label == expected_output.outputs.label


@pytest.mark.order(3)
def test_served_iptc_model_bio(
    test_model_name, test_served_model_artifacts, test_model_card
):
    """Tests the fully initialized and loaded ServedIPTCModel's bio method."""
    served_iptc_model = ServedIPTCModel(
        served_model_artifacts=test_served_model_artifacts
    )

    served_iptc_model.load()

    actual_output = served_iptc_model.bio()
    expected_output = BioResponseModel(
        model_name=test_model_name, model_card=test_model_card
    )

    assert actual_output == expected_output
