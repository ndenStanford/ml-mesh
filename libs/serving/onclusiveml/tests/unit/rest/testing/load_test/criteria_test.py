"""Criteria tests."""

# 3rd party libraries
import pytest

# Internal libraries
from libs.serving.onclusiveml.serving.rest.testing.load_test import (
    LoadTestCriteria,
)


@pytest.mark.parametrize(
    "test_criteria,test_n_criteria_expected", [([], 0), ([1, 2, 3], 3)]
)
def test_load_test_criteria(test_criteria, test_n_criteria_expected):
    """Tests the initialization of a LoadTestCriteria instance."""
    load_test_criteria = LoadTestCriteria(criteria=test_criteria)

    assert load_test_criteria.n_criteria == test_n_criteria_expected
