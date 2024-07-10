"""Constants Tests."""

# Source
from src.model.constants import MODELS_TO_PARAMETERS, ChatModel


def test_all_models_in_parameters_map():
    """Test if all models have corresponding parameters class."""
    for model in ChatModel:
        if isinstance(model, str):
            assert (
                model in MODELS_TO_PARAMETERS
            ), f"{model} is not in MODELS_TO_PARAMETERS"
