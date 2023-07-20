# 3rd party libraries
import pytest

# Source
from src.served_model import ServedNERModel
from src.server_models import (
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
    """Tests the constructor of the ServedNERModel, EXCLUDING the loading of genuine model
    artifacts from local disk"""

    ServedNERModel(served_model_artifacts=test_served_model_artifacts)


@pytest.mark.order(2)
def test_served_ner_model_load(test_served_model_artifacts):
    """Tests the constructor of the ServedNERModel, INCLUDING the loading of genuine model
    artifacts from local disk"""

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
    """Tests the fully initialized and loaded ServedNERModel's predict method, using the
    custom data models for validation and the test files from the model artifact as ground truth
    for the regression test element."""

    served_ner_model = ServedNERModel(
        served_model_artifacts=test_served_model_artifacts
    )
    served_ner_model.load()
    input = PredictRequestModel(
        configuration=PredictConfiguration(
            return_pos=test_inference_params["return_pos"]
        ),
        inputs=PredictInputContentModel(content=test_inputs[test_record_index]),
    )

    actual_output = served_ner_model.predict(input)

    expected_output = PredictResponseModel(
        outputs=PredictionOutputContent(
            predicted_content=[
                PredictionExtractedEntity(
                    entity_type=i["entity_type"],
                    entity_text=i["entity_text"],
                    score=i["score"],
                    sentence_index=i["sentence_index"],
                    start=i["start"],
                    end=i["end"],
                )
                for i in test_predictions[test_record_index]
            ]
        )
    )

    assert actual_output == expected_output


@pytest.mark.order(3)
def test_served_ner_model_bio(
    test_model_name, test_served_model_artifacts, test_model_card
):
    """Tests the fully initialized and loaded ServedNERModel's bio method, using the
    custom data models for validation and the model card from the model artifact as ground truth
    for the regression test element."""

    served_ner_model = ServedNERModel(
        served_model_artifacts=test_served_model_artifacts
    )

    served_ner_model.load()

    actual_output = served_ner_model.bio()
    expected_output = BioResponseModel(
        model_name=test_model_name, model_card=test_model_card
    )

    assert actual_output == expected_output
