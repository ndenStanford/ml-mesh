# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.testing import LoadTestCriteria


@pytest.mark.parametrize(
    "test_criteria,test_n_criteria_expected", [([], 0), ([1, 2, 3], 3)]
)
def test_load_test_criteria(test_criteria, test_n_criteria_expected):

    load_test_criteria = LoadTestCriteria(criteria=test_criteria)

    assert load_test_criteria.n_criteria == test_n_criteria_expected
