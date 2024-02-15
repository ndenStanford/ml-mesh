"""Prediction model tests."""
# isort: skip_file

# 3rd party libraries
import pytest

# Source
from src.generate_trend import single_topic_trend


@pytest.mark.order(1)
def test_generate_trendy_predict(
    test_all_topic_count_input, test_df_all_count_list_input
):
    """Test get_trendy function."""
    test_actual_predict_output = [
        single_topic_trend(test_all_topic_count_input, df_all_count)
        for df_all_count in test_df_all_count_list_input
    ]
    print(test_actual_predict_output)
    assert test_actual_predict_output == [True, False, False]
