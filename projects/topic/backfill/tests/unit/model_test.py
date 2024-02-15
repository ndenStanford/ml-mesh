"""Prediction model tests."""
# isort: skip_file

# 3rd party libraries
import pytest

# Source
from src.generate_trend import get_trendy


@pytest.mark.order(1)
def test_generate_trendy_predict(
    test_all_topic_count_input, test_df_all_count_dict_input, test_keyword_input
):
    """Test get_trendy function."""
    test_actual_predict_output = get_trendy(
        test_all_topic_count_input, test_df_all_count_dict_input, test_keyword_input
    )
    print(test_actual_predict_output)
