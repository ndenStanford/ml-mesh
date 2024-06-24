# Standard Library
from unittest.mock import patch

# Internal libraries
from onclusiveml.tracking.optimization import OnclusiveModelOptimizer


@patch(
    "onclusiveml.tracking.optimization.OnclusiveModelOptimizer.create_tracked_model_version",
    return_value=None,
)
def test_onclusive_model_optimizer_initialize(
    mock_create_tracked_model_version, tracked_model_settings, tracked_model_card
):
    optimizer = OnclusiveModelOptimizer(tracked_model_settings, tracked_model_card)
    assert optimizer.tracked_model_settings == tracked_model_settings
    assert optimizer.model_card == tracked_model_card
    mock_create_tracked_model_version.assert_called_once()
