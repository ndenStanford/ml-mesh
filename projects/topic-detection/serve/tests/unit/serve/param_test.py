"""Unit test inference and aggregate."""
# isort: skip_file

# Standard Library
from unittest.mock import patch

# Source
from src.serve.topic import TopicHandler

_service = TopicHandler()


@patch("requests.post")
def test_handler_inference(mock_post, article_input, model_card):
    """Test the inference function in topic handler."""
    mock_post.return_value = model_card

    gpt_inference = _service.inference(
        article=article_input,
        cate="Opportunities",
        industry="Science and technology",
    )
    assert isinstance(gpt_inference, str)


@patch("requests.post")
def test_handler_aggregate(mock_post, article_input, model_card):
    """Test the aggregate function in handler."""
    mock_post.return_value = model_card
    gpt_inference = _service.aggregate(
        article=article_input,
        industry="Science and technology",
    )
    assert isinstance(gpt_inference, dict)
