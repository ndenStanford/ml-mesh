"""Model types tests."""

# Internal libraries
from onclusiveml.tracking.tracked_model_utils import ModelTypes


def test_get_valid_range():

    assert ModelTypes.get_valid_range() == ("base", "trained", "compiled")
