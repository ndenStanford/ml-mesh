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


def test_served_keywords_model__init__(test_served_model_params):

    ServedKeywordsModel(served_model_params=test_served_model_params)


def test_served_keywords_model_load(test_served_model_params):

    served_keywords_model = ServedKeywordsModel(
        served_model_params=test_served_model_params
    )

    assert not served_keywords_model.is_ready()

    served_keywords_model.load()

    assert served_keywords_model.is_ready()


@pytest.mark.parametrize("test_record_index", [0, 1, 2])
def test_served_keywprds_model_predict(
    test_served_model_params,
    test_inputs,
    test_inference_params,
    test_predictions,
    test_record_index,
):

    served_keywords_model = ServedKeywordsModel(
        served_model_params=test_served_model_params
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


def test_served_keywprds_model_bio(
    test_model_name, test_served_model_params, test_model_card
):

    served_keywords_model = ServedKeywordsModel(
        served_model_params=test_served_model_params
    )

    served_keywords_model.load()

    actual_output = served_keywords_model.bio()
    expected_output = BioResponseModel(
        model_name=test_model_name, model_card=test_model_card
    )

    assert actual_output == expected_output
