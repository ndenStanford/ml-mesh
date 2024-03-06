"""Test BERTopic trainer."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.training import BertopicTrainer


@pytest.fixture
@patch(
    "onclusiveml.core.optimization.OnclusiveModelOptimizer.create_tracked_model_version",
    return_value=None,
)
def bertopic_trainer(
    mock_create_tracked_model_version,
    tracked_model_specs,
    tracked_model_card,
    feature_store_params,
):
    """Test Bertopic trainer initialization."""
    stopwords = ["a", "an", "the"]
    bertopic_trainer = BertopicTrainer(
        tracked_model_specs=tracked_model_specs,
        model_card=tracked_model_card,
        data_fetch_params=feature_store_params,
        stopwords=stopwords,
    )
    mock_create_tracked_model_version.assert_called_once()
    return bertopic_trainer


def test_bertopic_trainer_init(
    bertopic_trainer, tracked_model_specs, tracked_model_card, feature_store_params
):
    """Test Bertopic trainer internal variables."""
    assert bertopic_trainer.tracked_model_specs == tracked_model_specs
    assert bertopic_trainer.model_card == tracked_model_card
    assert bertopic_trainer.data_fetch_params == feature_store_params
    assert bertopic_trainer.stopwords == ["a", "an", "the"]
