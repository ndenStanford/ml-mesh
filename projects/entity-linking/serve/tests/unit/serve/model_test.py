"""Model test."""

# Standard Library
from unittest.mock import patch, MagicMock

# 3rd party libraries
import pytest
from pytest_unordered import unordered

# Source
from src.serve.model import ServedBelaModel
from src.serve.schemas import PredictRequestSchema, PredictResponseSchema
from onclusiveml.serving.rest.serve import OnclusiveHTTPException


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


(
    {
        "content": "Steve Jobs was CEO of Apple",
        "entities": [
            {
                "entity_type": "Pers",
                "text": "Steve Jobs",
                "salience_score": 0.9259419441223145,
                "sentence_indexes": [0],
            },
            {
                "entity_type": "ORG",
                "text": "Apple",
                "salience_score": 0.9259419441223145,
                "sentence_indexes": [0],
            }
        ]
    },
    {
        "version": 1,  
        "namespace": "entity-linking",
        "data": {
            "identifier": None,
            "namespace": "entity-linking",
            "attributes": {
                "entities": [
                    {
                        "entity_type": "Pers",
                        "text": "CEO",
                        "salience_score": 0.24852901697158813,
                        "sentence_indexes": [0],
                        "wiki_link": "https://www.wikidata.org/wiki/Q484876",
                        "wiki_score": 0.48496711254119873
                    },
                    {
                        "entity_type": "ORG",
                        "text": "Apple",
                        "salience_score": 0.7043066024780273,
                        "sentence_indexes": [0],
                        "wiki_link": "https://www.wikidata.org/wiki/Q312",
                        "wiki_score": 0.9504453539848328
                    }
                ]
            }
        }
    }
)
def test_predict(mock_served_model, payload, expected_output):
    predict_request = PredictRequestSchema(
        data={
            "identifier": None,
            "namespace": "entity-linking",
            "attributes": payload,
            "parameters": {"lang": "en"},
        }
    )

    predict_response = PredictResponseSchema(
        version= 1,
        data={
            "identifier": None,
            "namespace": "entity-linking",
            "attributes": expected_output,
        }
    )

    response = mock_served_model.predict(predict_request)

    assert response.version ==  expected_output["version"]
    assert response.data.identifier == expected_output["data"]["identifier"]
    assert response.data.namespace == expected_output["data"]["namespace"]
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
            "The language reference 'invalid_language' could not be mapped, or the language could not be inferred from the content.",
        )
    ],
)
def test_model_prediction_invalid_language(mock_served_model_with_exception, payload, expected_error_detail):

    predict_request = PredictRequestSchema(**payload)

    with pytest.raises(OnclusiveHTTPException) as exc_info:
        mock_served_model_with_exception.predict(predict_request)

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == expected_error_detail