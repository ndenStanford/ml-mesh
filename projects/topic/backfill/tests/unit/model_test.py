"""Prediction model tests."""
# isort: skip_file

# 3rd party libraries
import pytest

# Source
from src.__main__ import TrendDetection

trend = TrendDetection()


@pytest.mark.order(1)
def test_generate_trendy_predict(
    test_df_all_topic_input, test_df_single_topic_list_input
):
    """Test get_trendy function."""
    test_actual_predict_output = [
        trend.single_topic_trend(df_single_topic, test_df_all_topic_input)
        for df_single_topic in test_df_single_topic_list_input
    ]
    assert test_actual_predict_output == [True, False, False]
