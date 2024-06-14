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
from src.serve.impact_quantification import ImpactQuantification
from onclusiveml.serving.serialization.topic_summarization.v1 import ImpactCategoryLabel
from onclusiveml.data.query_profile import (
    StringQueryProfile,
    ProductionToolsQueryProfile,
)
from src.settings import get_settings

_service = TopicHandler()
settings = get_settings()


@patch("requests.post")
def test_handler_inference(mock_post, article_input, mock_responses):
    """Test the inference function in topic handler."""
    mock_post.return_value = mock_responses

    gpt_inference = _service.topic_inference(
        articles=article_input,
    )
    assert isinstance(gpt_inference, dict)


@patch("requests.post")
def test_handler_summary(mock_post, article_input, mock_responses):
    """Test the summary function in topic handler."""
    mock_post.return_value = mock_responses

    gpt_inference = _service.summary_inference(
        articles=article_input,
    )
    assert isinstance(gpt_inference, dict)


@patch("requests.post")
def test_claude_gpt_switch(
    mock_post, mock_claude_fail_output, mock_responses, article_input
):
    """Test prompt routing logic."""
    mock_claude_response = mock_claude_fail_output
    mock_gpt_response = mock_responses
    mock_post.side_effect = [mock_claude_response, mock_gpt_response]
    gpt_inference = _service.topic_inference(
        articles=article_input,
    )
    assert isinstance(gpt_inference, dict)


@patch("requests.post")
def test_handler_aggregate(mock_post, article_input, mock_responses):
    """Test the aggregate function in handler."""
    mock_post.return_value = mock_responses
    gpt_inference = _service.aggregate(
        article=article_input,
    )
    assert isinstance(gpt_inference, dict)


@patch("requests.put")
@patch("requests.get")
@patch("src.serve.trend_detection.Elasticsearch")
@pytest.mark.parametrize(
    "profile, topic_id, start_time, end_time",
    [
        (
            StringQueryProfile(
                string_query="""("Apple Music" OR AppleMusic) AND sourcecountry:[ESP,AND] AND sourcetype:print"""  # noqa: E501
            ),
            562,
            pd.Timestamp.now(),
            pd.Timestamp.now() - pd.Timedelta(days=14),
        ),
    ],
)
def test_not_trending(
    mock_elasticsearch,
    mock_get,
    mock_put,
    profile,
    topic_id,
    start_time,
    end_time,
    mock_boolean_query_translated,
    mock_boolean_check,
    mock_topic_profile_es_result_not_trending,
    mock_profile_es_result,
):
    """Test single topic trend function."""
    mock_get.return_value = mock_boolean_query_translated
    mock_put.return_value = mock_boolean_check
    mock_elasticsearch.return_value.search.side_effect = [
        mock_profile_es_result,
        mock_topic_profile_es_result_not_trending,
    ]
    trend_detector = TrendDetection()
    res = trend_detector.single_topic_trend(
        profile,
        topic_id,
        start_time,
        end_time,
        settings.TOPIC_DOCUMENT_THRESHOLD,
        settings.TREND_TIME_INTERVAL,
    )
    assert res[0] is False
    assert res[1] is None


@patch("requests.put")
@patch("requests.get")
@patch("src.serve.trend_detection.Elasticsearch")
@pytest.mark.parametrize(
    "profile, topic_id, start_time, end_time",
    [
        (
            StringQueryProfile(
                string_query="""("Apple Music" OR AppleMusic) AND sourcecountry:[ESP,AND] AND sourcetype:print"""  # noqa: E501
            ),
            562,
            pd.Timestamp.now(),
            pd.Timestamp.now() - pd.Timedelta(days=14),
        ),
    ],
)
def test_trending(
    mock_elasticsearch,
    mock_get,
    mock_put,
    profile,
    topic_id,
    start_time,
    end_time,
    mock_boolean_query_translated,
    mock_boolean_check,
    mock_topic_profile_es_result_trending,
    mock_profile_es_result,
):
    """Test single topic trend function."""
    mock_get.return_value = mock_boolean_query_translated
    mock_put.return_value = mock_boolean_check
    mock_elasticsearch.return_value.search.side_effect = [
        mock_profile_es_result,
        mock_topic_profile_es_result_trending,
    ]
    trend_detector = TrendDetection()
    res = trend_detector.single_topic_trend(
        profile,
        topic_id,
        start_time,
        end_time,
        settings.TOPIC_DOCUMENT_THRESHOLD,
        settings.TREND_TIME_INTERVAL,
    )
    assert res[0] is True
    assert res[1] == pd.Timestamp("2024-03-25 12:00:00+0000")


@patch("requests.put")
@patch("requests.get")
@patch("src.serve.trend_detection.Elasticsearch")
@pytest.mark.parametrize(
    "profile, topic_id, start_time, end_time",
    [
        (
            ProductionToolsQueryProfile(
                version="1",
                query_id="b529bdd8-47fd-4dbe-b105-53a02ced41cc",  # noqa: E501
            ),
            562,
            pd.Timestamp.now(),
            pd.Timestamp.now() - pd.Timedelta(days=14),
        ),
    ],
)
def test_not_trending_query_id(
    mock_elasticsearch,
    mock_get,
    mock_put,
    profile,
    topic_id,
    start_time,
    end_time,
    mock_boolean_query_translated,
    mock_boolean_check,
    mock_reponses_production_tool,
    mock_topic_profile_es_result_not_trending,
    mock_profile_es_result,
):
    """Test single topic trend function."""
    mock_get.side_effect = [
        mock_reponses_production_tool,
        mock_boolean_query_translated,
    ]
    mock_put.return_value = mock_boolean_check
    mock_elasticsearch.return_value.search.side_effect = [
        mock_profile_es_result,
        mock_topic_profile_es_result_not_trending,
    ]
    trend_detector = TrendDetection()
    res = trend_detector.single_topic_trend(
        profile,
        topic_id,
        start_time,
        end_time,
        settings.TOPIC_DOCUMENT_THRESHOLD,
        settings.TREND_TIME_INTERVAL,
    )
    assert res[0] is False
    assert res[1] is None


@patch("requests.put")
@patch("requests.get")
@patch("src.serve.trend_detection.Elasticsearch")
@pytest.mark.parametrize(
    "profile, topic_id, start_time, end_time",
    [
        (
            ProductionToolsQueryProfile(
                version="1",
                query_id="b529bdd8-47fd-4dbe-b105-53a02ced41cc",  # noqa: E501
            ),
            562,
            pd.Timestamp.now(),
            pd.Timestamp.now() - pd.Timedelta(days=14),
        ),
    ],
)
def test_trending_query_id(
    mock_elasticsearch,
    mock_get,
    mock_put,
    profile,
    topic_id,
    start_time,
    end_time,
    mock_boolean_query_translated,
    mock_boolean_check,
    mock_reponses_production_tool,
    mock_topic_profile_es_result_trending,
    mock_profile_es_result,
):
    """Test single topic trend function."""
    mock_get.side_effect = [
        mock_reponses_production_tool,
        mock_boolean_query_translated,
    ]
    mock_put.return_value = mock_boolean_check
    mock_elasticsearch.return_value.search.side_effect = [
        mock_profile_es_result,
        mock_topic_profile_es_result_trending,
    ]
    trend_detector = TrendDetection()
    res = trend_detector.single_topic_trend(
        profile,
        topic_id,
        start_time,
        end_time,
        settings.TOPIC_DOCUMENT_THRESHOLD,
        settings.TREND_TIME_INTERVAL,
    )
    assert res[0] is True
    assert res[1] == pd.Timestamp("2024-03-25 12:00:00+0000")


@patch("requests.put")
@patch("requests.get")
@patch("src.serve.impact_quantification.Elasticsearch")
@pytest.mark.parametrize(
    "profile, topic_id",
    [
        (
            StringQueryProfile(
                string_query="""("Apple Music" OR AppleMusic) AND sourcecountry:[ESP,AND] AND sourcetype:print"""  # noqa: E501
            ),
            562,
        ),
    ],
)
def test_impact_quantification(
    mock_elasticsearch,
    mock_get,
    mock_put,
    profile,
    topic_id,
    mock_boolean_query_translated,
    mock_boolean_check,
    mock_all_global_query,
    mock_topic_global_query,
    mock_all_profile_boolean_query,
    mock_topic_profile_query,
):
    """Test single topic trend function."""
    mock_get.return_value = mock_boolean_query_translated
    mock_put.return_value = mock_boolean_check
    mock_elasticsearch.return_value.search.side_effect = [
        mock_all_global_query,
        mock_topic_global_query,
        mock_all_profile_boolean_query,
        mock_topic_profile_query,
    ]
    trend_detector = ImpactQuantification()
    res = trend_detector.quantify_impact(profile, topic_id)
    assert res == ImpactCategoryLabel.LOW
