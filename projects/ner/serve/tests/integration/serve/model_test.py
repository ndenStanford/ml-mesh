"""Served model test."""

# 3rd party libraries
import pytest

# Source
from src.serve.served_model import ServedNERModel
from src.serve.server_models import (
    BioResponseModel,
    PredictConfiguration,
    PredictInputContentModel,
    PredictionExtractedEntity,
    PredictionOutputContent,
    PredictRequestModel,
    PredictResponseModel,
)


@pytest.mark.order(1)
def test_served_ner_model__init__(test_served_model_artifacts):
    """Tests the constructor of the ServedNERModel."""
    ServedNERModel(served_model_artifacts=test_served_model_artifacts)


@pytest.mark.order(2)
def test_served_ner_model_load(test_served_model_artifacts):
    """Tests the constructor of the ServedNERModel."""
    served_ner_model = ServedNERModel(
        served_model_artifacts=test_served_model_artifacts
    )

    assert not served_ner_model.is_ready()

    served_ner_model.load()

    assert served_ner_model.is_ready()


@pytest.mark.parametrize("test_record_index", [0, 1, 2])
def test_served_ner_model_predict(
    test_served_model_artifacts,
    test_inputs,
    test_inference_params,
    test_predictions,
    test_record_index,
):
    """Tests the fully initialized and loaded ServedNERModel's predict method."""
    served_ner_model = ServedNERModel(
        served_model_artifacts=test_served_model_artifacts
    )
    served_ner_model.load()
    input = PredictRequestModel(
        configuration=PredictConfiguration(return_pos=True, language="en"),
        inputs=PredictInputContentModel(content=test_inputs[test_record_index]),
    )

    actual_output = served_ner_model.predict(input)

    expected_output = PredictResponseModel(
        outputs=PredictionOutputContent(
            predicted_content=[
                PredictionExtractedEntity(**i)
                for i in test_predictions[test_record_index]
            ]
        )
    )

    assert actual_output == expected_output


@pytest.mark.parametrize("test_record_index", [0, 1, 2])
def test_served_ner_model_predict_no_pos(
    test_served_model_artifacts,
    test_inputs,
    test_inference_params,
    test_predictions,
    test_record_index,
):
    """Tests the fully initialized and loaded ServedNERModel's predict method."""
    served_ner_model = ServedNERModel(
        served_model_artifacts=test_served_model_artifacts
    )
    served_ner_model.load()
    input = PredictRequestModel(
        configuration=PredictConfiguration(return_pos=False, language="en"),
        inputs=PredictInputContentModel(content=test_inputs[test_record_index]),
    )

    actual_output = served_ner_model.predict(input)

    expected_output = PredictResponseModel(
        outputs=PredictionOutputContent(
            predicted_content=[
                PredictionExtractedEntity(**i)
                for i in test_predictions[test_record_index]
            ]
        )
    )
    assert (
        expected_output.outputs.predicted_content[0].entity_type
        == actual_output.outputs.predicted_content[0].entity_type  # noqa: W503
    )
    assert (
        expected_output.outputs.predicted_content[0].entity_text
        == actual_output.outputs.predicted_content[0].entity_text  # noqa: W503
    )
    assert (
        expected_output.outputs.predicted_content[0].score
        == actual_output.outputs.predicted_content[0].score  # noqa: W503
    )
    assert (
        expected_output.outputs.predicted_content[0].sentence_index
        == actual_output.outputs.predicted_content[0].sentence_index  # noqa: W503
    )
    assert "start" not in actual_output.outputs.predicted_content[0]
    assert "end" not in actual_output.outputs.predicted_content[0]


@pytest.mark.order(3)
def test_served_ner_model_bio(
    test_model_name, test_served_model_artifacts, test_model_card
):
    """Tests the fully initialized and loaded ServedNERModel's bio method."""
    served_ner_model = ServedNERModel(
        served_model_artifacts=test_served_model_artifacts
    )

    served_ner_model.load()

    actual_output = served_ner_model.bio()
    expected_output = BioResponseModel(
        model_name=test_model_name, model_card=test_model_card
    )

    assert actual_output == expected_output
