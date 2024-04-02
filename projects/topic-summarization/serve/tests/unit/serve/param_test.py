"""Unit test inference and aggregate."""
# isort: skip_file

# Standard Library
from unittest.mock import patch
import pytest

# 3rd party libraries
import pandas as pd

# Source
from src.serve.topic import TopicHandler
from src.serve.trend_detection import TrendDetection

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


@patch("requests.post")
@patch("src.serve.trend_detection.Elasticsearch")
@pytest.mark.parametrize(
    "profile_id, topic_id, start_time, end_time",
    [
        (
            """("Apple Music" OR AppleMusic) AND sourcecountry:[ESP,AND] AND sourcetype:print""",
            562,
            pd.Timestamp.now(),
            pd.Timestamp.now() - pd.Timedelta(days=14),
        ),
    ],
)
def test_not_trending(
    mock_elasticsearch,
    mock_post,
    profile_id,
    topic_id,
    start_time,
    end_time,
    mock_boolean_query_translated,
    mock_topic_profile_es_result_not_trending,
    mock_profile_es_result,
):
    """Test single topic trend function."""
    mock_post.return_value = mock_boolean_query_translated
    mock_elasticsearch.return_value.search.side_effect = [
        mock_profile_es_result,
        mock_topic_profile_es_result_not_trending,
    ]
    trend_detector = TrendDetection()
    res = trend_detector.single_topic_trend(profile_id, topic_id, start_time, end_time)
    assert res == (False, None)


@patch("requests.post")
@patch("src.serve.trend_detection.Elasticsearch")
@pytest.mark.parametrize(
    "profile_id, topic_id, start_time, end_time",
    [
        (
            """("Apple Music" OR AppleMusic) AND sourcecountry:[ESP,AND] AND sourcetype:print""",
            562,
            pd.Timestamp.now(),
            pd.Timestamp.now() - pd.Timedelta(days=14),
        ),
    ],
)
def test_trending(
    mock_elasticsearch,
    mock_post,
    profile_id,
    topic_id,
    start_time,
    end_time,
    mock_boolean_query_translated,
    mock_topic_profile_es_result_trending,
    mock_profile_es_result,
):
    """Test single topic trend function."""
    mock_post.return_value = mock_boolean_query_translated
    mock_elasticsearch.return_value.search.side_effect = [
        mock_profile_es_result,
        mock_topic_profile_es_result_trending,
    ]
    trend_detector = TrendDetection()
    res = trend_detector.single_topic_trend(profile_id, topic_id, start_time, end_time)
    assert res == (True, pd.Timestamp("2024-03-25 12:00:00+0000"))
