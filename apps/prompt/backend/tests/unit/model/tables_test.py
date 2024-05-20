"""Table tests."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
from langchain_core.language_models.chat_models import BaseChatModel

# Source
from src.model.tables import LanguageModel


@pytest.mark.parametrize(
    "alias, provider",
    [
        ("model-1", "openai"),
        ("model-2", "openai"),
        ("model-3", "bedrock"),
    ],
)
@patch("boto3.setup_default_session")
@patch("boto3.client")
def test_as_langchain(boto3_client_mock, boto3_mock, alias, provider):
    """Test langchain compatible mixin."""
    llm = LanguageModel(alias=alias, provider=provider)
    assert isinstance(llm.as_langchain(), BaseChatModel)
