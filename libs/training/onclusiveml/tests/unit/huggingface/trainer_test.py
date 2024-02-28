"""Test Huggingface trainer."""

# Standard Library
from unittest.mock import patch

# Internal libraries
from libs.training.onclusiveml.training.huggingface.trainer import (
    OnclusiveHuggingfaceModelTrainer,
)


@patch(
    "onclusiveml.core.optimization.OnclusiveModelOptimizer.create_tracked_model_version",
    return_value=None,
)
def test_onclusive_huggingface_model_trainer_initialize(
    mock_create_tracked_model_version,
    tracked_model_specs,
    tracked_model_card,
    feature_store_params,
):
    """Test Huggingface trainer initialization."""
    trainer = OnclusiveHuggingfaceModelTrainer(
        tracked_model_specs, tracked_model_card, feature_store_params
    )
    assert trainer.tracked_model_specs == tracked_model_specs
    assert trainer.model_card == tracked_model_card
    assert trainer.data_fetch_params == feature_store_params
    mock_create_tracked_model_version.assert_called_once()
