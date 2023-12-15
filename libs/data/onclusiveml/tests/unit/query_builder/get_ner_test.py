"""NER Test."""

# Standard Library
from unittest.mock import Mock, patch

# 3rd party libraries
import pytest  # noqa

# Internal libraries
from onclusiveml.query_builder import predict_ner


# Mocking the API response for successful case
@patch("onclusiveml.query_builder.get_ner.requests.post")
def test_predict_ner_success(mock_post):
    """Mock test NER."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "identifier": None,
            "namespace": "ner",
            "attributes": {
                "entities": [
                    {
                        "entity_type": "ORG",
                        "entity_text": "Apple",
                        "score": 0.9979469299316406,
                        "sentence_index": 0,
                        "start": 32,
                        "end": 36,
                    },
                    {
                        "entity_type": "ORG",
                        "entity_text": "Microsoft",
                        "score": 0.9912342314132445,
                        "sentence_index": 0,
                        "start": 42,
                        "end": 50,
                    },
                ]
            },
        }
    }
    mock_post.return_value = mock_response

    result = predict_ner(
        "This is a dummy sentence with Apple and Microsoft.", ["Apple", "Microsoft"]
    )
    assert result == ["Apple", "Microsoft"]


# Mocking the API response for failure case
@patch("onclusiveml.query_builder.get_ner.requests.post")
def test_predict_ner_failure(mock_post):
    """Mock test NER."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_post.return_value = mock_response
    # Testing predict_ner function for failure scenario
    try:
        predict_ner(
            "This is a dummy sentence with Apple and Microsoft.", ["Apple", "Microsoft"]
        )
    except ValueError as e:
        assert str(e) == "Error in stage endpoint"
    else:
        assert False, "Exception not raised"
