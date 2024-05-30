"""Model test."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import OnclusiveHTTPException

# Source
from src.serve.model import TranslationModel
from src.serve.schemas import PredictRequestSchema, PredictResponseSchema
from src.settings import get_settings


settings = get_settings()


def test_model_bio(translation_model):
    """Model bio test."""
    assert translation_model.bio().dict() == {
        "version": 1,
        "data": {
            "namespace": "translation",
            "identifier": None,
            "attributes": {
                "model_name": "translation",
            },
        },
    }


@pytest.mark.parametrize(
    "payload, predict_return, expected_response",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "content": "Tottenham Hotspur Football Club has drawn up plans for student flats on the site of a former printworks near its stadium.",  # noqa
                        "target_lang": "fr",
                    },
                    "parameters": {
                        "lang": "en",
                        "brievety": False,
                        "lang_detect": False,
                        "translation": True,
                    },
                }
            },
            "Le Tottenham Hotspur Football Club a élaboré des plans pour des appartements étudiants sur le site d'une ancienne imprimerie à proximité de son stade.",  # noqa
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "original_language": "en",
                        "target_language": "fr",
                        "translation": "Le Tottenham Hotspur Football Club a élaboré des plans pour des appartements étudiants sur le site d'une ancienne imprimerie à proximité de son stade.",  # noqa
                    },
                },
            },
        )
    ],
)
@patch.object(TranslationModel, "_predict")
def test_model_predict(
    mock_predict, translation_model, payload, predict_return, expected_response
):
    """Test model predict."""
    mock_predict.return_value = predict_return

    attributes = payload["data"]["attributes"]
    parameters = payload["data"]["parameters"]

    response = translation_model.predict(PredictRequestSchema(**payload))

    mock_predict.assert_called_with(
        content=attributes["content"],
        original_language=parameters["lang"],
        target_language=attributes["target_lang"],
        brievety=parameters["brievety"],
    )

    assert response == PredictResponseSchema(**expected_response)


@pytest.mark.parametrize(
    "payload,expected_error_detail",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "content": "Irrelevant content because of invalid message value (nonsense).",  # noqa
                        "target_lang": "fr",
                    },
                    "parameters": {
                        "lang": "invalid_language",
                        "brievety": False,
                        "lang_detect": False,
                        "translation": True,
                    },
                }
            },
            "The language reference 'invalid_language' could not be mapped, or the language could not be inferred from the content.",  # noqa
        )
    ],
)
def test_model_prediction_invalid_language(
    mock_served_model_with_exception, payload, expected_error_detail  # noqa
):
    """Testing invalid language test."""
    predict_request = PredictRequestSchema(**payload)

    with pytest.raises(OnclusiveHTTPException) as exc_info:
        mock_served_model_with_exception.predict(predict_request)

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == expected_error_detail


@patch("src.serve.model.detect_language")
def test_detect_language(mock_detect_language, translation_model):
    """Test _detect_language method."""
    mock_detect_language.return_value = "en"
    content = "Le Tottenham Hotspur Football Club a élaboré des plans pour des appartements étudiants sur le site d'une ancienne imprimerie à proximité de son stade."  # noqa

    detected_language = translation_model._detect_language(content)

    mock_detect_language.assert_called_once_with(content=content)
    assert detected_language == "en"
