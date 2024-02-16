"""Prediction model tests."""
# isort: skip_file

# 3rd party libraries
import pytest

# Source
from src.generate_trend import TrendDetection

trend = TrendDetection()


@pytest.mark.order(1)
def test_generate_trendy_predict(
    test_all_topic_count_input, test_df_all_count_list_input
):
    """Test get_trendy function."""
    test_actual_predict_output = [
        trend.single_topic_trend(df_all_count, test_all_topic_count_input)
        for df_all_count in test_df_all_count_list_input
    ]
    assert test_actual_predict_output == [True, False, False]
