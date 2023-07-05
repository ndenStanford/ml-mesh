# 3rd party libraries
import pytest

# Source
from src.served_model import ServedKeywordsModel
from src.server_models import (
    BioResponseModel,
    PredictConfiguration,
    PredictInputDocumentModel,
    PredictionExtractedKeyword,
    PredictionOutputDocument,
    PredictRequestModel,
    PredictResponseModel,
)


@pytest.mark.order(1)
def test_served_keywords_model__init__(test_served_model_artifacts):
    """Tests the constructor of the ServedKeywordsModel, EXCLUDING the loading of genuine model
    artifacts from local disk"""

    ServedKeywordsModel(served_model_artifacts=test_served_model_artifacts)


@pytest.mark.order(2)
def test_served_keywords_model_load(test_served_model_artifacts):
    """Tests the constructor of the ServedKeywordsModel, INCLUDING the loading of genuine model
    artifacts from local disk"""

    served_keywords_model = ServedKeywordsModel(
        served_model_artifacts=test_served_model_artifacts
    )

    assert not served_keywords_model.is_ready()

    served_keywords_model.load()

    assert served_keywords_model.is_ready()


@pytest.mark.order(3)
@pytest.mark.parametrize("test_record_index", [0, 1, 2])
def test_served_keywords_model_predict(
    test_served_model_artifacts,
    test_inputs,
    test_inference_params,
    test_predictions,
    test_record_index,
):
    """Tests the fully initialized and loaded ServedKeywordsModel's predict method, using the
    custom data models for validation and the test files from the model artifact as ground truth
    for the regression test element."""

    served_keywords_model = ServedKeywordsModel(
        served_model_artifacts=test_served_model_artifacts
    )
    served_keywords_model.load()

    input = PredictRequestModel(
        configuration=PredictConfiguration(**test_inference_params),
        inputs=[PredictInputDocumentModel(document=test_inputs[test_record_index])],
    )

    actual_output = served_keywords_model.predict(input)

    expected_output = PredictResponseModel(
        outputs=[
            PredictionOutputDocument(
                predicted_document=[
                    PredictionExtractedKeyword(keyword_token=kt, keyword_score=ks)
                    for kt, ks in test_predictions[test_record_index]
                ]
            )
        ]
    )

    assert actual_output == expected_output


@pytest.mark.order(3)
def test_served_keywords_model_bio(
    test_model_name, test_served_model_artifacts, test_model_card
):
    """Tests the fully initialized and loaded ServedKeywordsModel's bio method, using the
    custom data models for validation and the model card from the model artifact as ground truth
    for the regression test element."""

    served_keywords_model = ServedKeywordsModel(
        served_model_artifacts=test_served_model_artifacts
    )

    served_keywords_model.load()

    actual_output = served_keywords_model.bio()
    expected_output = BioResponseModel(
        model_name=test_model_name, model_card=test_model_card
    )

    assert actual_output == expected_output
