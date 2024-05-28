"""Model test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import OnclusiveHTTPException

# Source
from src.serve.schemas import PredictRequestSchema, PredictResponseSchema


def test_model_bio(entity_linking_model):
    """Model bio test."""
    assert entity_linking_model.bio().dict() == {
        "version": 1,
        "data": {
            "namespace": "entity-linking",
            "identifier": None,
            "attributes": {
                "model_name": "entity-linking",
            },
        },
    }


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "content": "House prices were unchanged last month, defying predictions of another drop, but they are unlikely to have troughed just yet.",  # noqa
                "entities": [],
            },
            {"entities": []},
        ),
    ],
)
def test_predict_empty_return(mock_served_model_empty, payload, expected_response):
    """Testing model predictions."""
    predict_request = PredictRequestSchema(
        data={
            "identifier": None,
            "namespace": "entity-linking",
            "attributes": payload,
            "parameters": {"lang": "en"},
        }
    )

    response = mock_served_model_empty.predict(predict_request)

    predict_response = PredictResponseSchema(
        version=1,
        data={
            "identifier": None,
            "namespace": "entity-linking",
            "attributes": expected_response,
        },
    )

    assert response == predict_response


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "content": "Steve Jobs was CEO of Apple",
                "entities": [
                    {
                        "entity_type": "Pers",
                        "entity_text": "Steve Jobs",
                        "   score": 0.9259419441223145,
                        "sentence_index": [0],
                    },
                    {
                        "entity_type": "ORG",
                        "entity_text": "Apple",
                        "score": 0.9259419441223145,
                        "sentence_index": [0],
                    },
                ],
            },
            {
                "entities": [
                    {
                        "entity_type": "Pers",
                        "entity_text": "CEO",
                        "score": 0.24852901697158813,
                        "sentence_index": [0],
                        "wiki_link": "https://www.wikidata.org/wiki/Q484876",
                    },
                    {
                        "entity_type": "ORG",
                        "entity_text": "Apple",
                        "score": 0.7043066024780273,
                        "sentence_index": [0],
                        "wiki_link": "https://www.wikidata.org/wiki/Q312",
                    },
                ]
            },
        ),
    ],
)
def test_predict(mock_served_model, payload, expected_response):
    """Testing model predictions."""
    predict_request = PredictRequestSchema(
        data={
            "identifier": None,
            "namespace": "entity-linking",
            "attributes": payload,
            "parameters": {"lang": "en"},
        }
    )

    response = mock_served_model.predict(predict_request)

    predict_response = PredictResponseSchema(
        version=1,
        data={
            "identifier": None,
            "namespace": "entity-linking",
            "attributes": expected_response,
        },
    )

    assert response == predict_response


@pytest.mark.parametrize(
    "payload,expected_error_detail",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "content": "Irrelevant content because of invalid message value (nonsense)."
                    },
                    "parameters": {"lang": "invalid_language"},
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
