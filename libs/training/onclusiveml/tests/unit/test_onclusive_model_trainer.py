# Standard Library
from unittest.mock import patch

# Internal libraries
from onclusiveml.training.onclusive_model_trainer import OnclusiveModelTrainer


@patch(
    "onclusiveml.tracking.optimization.OnclusiveModelOptimizer.create_tracked_model_version",
    return_value=None,
)
def test_onclusive_model_trainer_initialize(
    mock_create_tracked_model_version,
    tracked_model_specs,
    tracked_model_card,
    feature_store_params,
):
    trainer = OnclusiveModelTrainer(
        tracked_model_specs, tracked_model_card, feature_store_params
    )
    assert trainer.tracked_model_specs == tracked_model_specs
    assert trainer.model_card == tracked_model_card
    assert trainer.data_fetch_params == feature_store_params
    mock_create_tracked_model_version.assert_called_once()
