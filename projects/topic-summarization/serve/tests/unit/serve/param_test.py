"""Unit test inference and aggregate."""
# isort: skip_file

# Standard Library
from unittest.mock import patch

# Source
from src.serve.topic import TopicHandler

_service = TopicHandler()


@patch("requests.post")
def test_handler_inference(mock_post, article_input, mock_responses):
    """Test the inference function in topic handler."""
    mock_post.return_value = mock_responses

    gpt_inference = _service.inference(
        article=article_input,
        category="Opportunities",
    )
    assert isinstance(gpt_inference, dict)


@patch("requests.post")
def test_handler_summary(mock_post, article_input, mock_responses):
    """Test the summary function in topic handler."""
    mock_post.return_value = mock_responses

    gpt_inference = _service.summary(
        article=article_input,
    )
    assert isinstance(gpt_inference, str)


@patch("requests.post")
def test_handler_topic_aggregate(mock_post, article_input, mock_responses_aggregate):
    """Test the aggregate function in handler."""
    mock_post.return_value = mock_responses_aggregate
    gpt_inference = _service.topic_aggregate(
        grouped_article=article_input,
    )
    assert isinstance(gpt_inference, dict)


@patch("requests.post")
def test_handler_summary_aggregate(mock_post, article_input, mock_responses):
    """Test the aggregate function in handler."""
    mock_post.return_value = mock_responses
    gpt_inference = _service.summary_aggregate(
        grouped_article=article_input,
    )
    assert isinstance(gpt_inference, dict)


@patch("requests.post")
def test_handler_aggregate(mock_post, article_input, mock_responses_aggregate):
    """Test the aggregate function in handler."""
    mock_post.return_value = mock_responses_aggregate
    gpt_inference = _service.aggregate(
        article=article_input,
    )
    assert isinstance(gpt_inference, dict)


def test_handler_group(article_input):
    """Test the group function in handler."""
    group_result = _service.group(
        article=article_input,
    )
    assert len(group_result) == 2
