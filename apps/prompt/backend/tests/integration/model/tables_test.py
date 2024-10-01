"""Model routes test."""

# 3rd party libraries
import pytest

# Source
from src.model.constants import DEFAULT_MODELS, ChatModel, ChatModelProdiver
from src.model.tables import LanguageModel


@pytest.mark.order(6)
def test_list_models(app):
    """Test get models."""
    assert len(list(LanguageModel.scan())) == len(DEFAULT_MODELS)


@pytest.mark.order(7)
@pytest.mark.parametrize(
    "alias, provider",
    [
        (ChatModel.CLAUDE_3_SONNET, ChatModelProdiver.BEDROCK),
        (ChatModel.GPT4_O, ChatModelProdiver.OPENAI),
    ],
)
def test_get_model(alias, provider, app):
    """Test get models."""
    llm = LanguageModel.get(alias)
    assert llm.provider == provider
