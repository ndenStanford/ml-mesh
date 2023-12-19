"""Entity-Linking Test."""

# Standard Library
from unittest.mock import Mock, patch

# 3rd party libraries
import pytest  # noqa

# Internal libraries
from onclusiveml.data.query_builder import predict_entity_linking


# Mocking the API response for successful case
@patch("onclusiveml.data.query_builder.get_el.requests.post")
def test_predict_entity_linking_success(mock_post):
    """Mock test Entity Linking."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "identifier": None,
            "namespace": "entity-linking",
            "attributes": {
                "entities": [{"wiki_link": "https://www.wikidata.org/wiki/Q312"}]
            },
        }
    }
    mock_post.return_value = mock_response

    result = predict_entity_linking("Apple")
    assert result == "https://www.wikidata.org/wiki/Q312"


# Mocking the API response for failure case
@patch("onclusiveml.data.query_builder.get_el.requests.post")
def test_predict_entity_linking_failure(mock_post):
    """Mock test Entity Linking."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_post.return_value = mock_response

    result = predict_entity_linking(
        "This is a dummy sentence about Apple, a tech company."
    )
    assert result is None
