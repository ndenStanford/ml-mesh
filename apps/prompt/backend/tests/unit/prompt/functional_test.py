"""Functional module tests."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
import redis
from langchain.chains import ConversationChain
from redis_cache import RedisCache

# Source
from src.model.tables import LanguageModel
from src.prompt import functional as F
from src.prompt.tables import PromptTemplate


@pytest.mark.parametrize(
    "project, prompt_alias, template, model_alias, provider",
    [
        ("new-project1", "prompt-1", "{text}", "gpt-4", "openai"),
        ("new-project2", "prompt-2", "{text}", "meta.llama2-70b-chat-v1", "bedrock"),
    ],
)
@patch.object(PromptTemplate, "get")
@patch.object(LanguageModel, "get")
@patch.object(ConversationChain, "predict")
@patch.object(RedisCache, "__call__")
@patch.object(redis.connection.ConnectionPool, "get_connection")
@patch("botocore.session.Session")
def test_generate_from_prompt_template(
    mock_boto_session,
    mock_redis_get_connection,
    mock_redis_client,
    mock_conversation_chain_predict,
    mock_model_get,
    mock_prompt_get,
    project,
    prompt_alias,
    template,
    model_alias,
    provider,
):
    """Test generate from prompt template."""
    mock_redis_get_connection.return_value.retry.call_with_retry.return_value = dict()
    mock_conversation_chain_predict.return_value = dict()
    mock_model_get.return_value = LanguageModel(alias=model_alias, provider=provider)
    mock_prompt_get.return_value = PromptTemplate(
        alias=prompt_alias, template=template, project=project
    )

    _ = F.generate_from_prompt_template(
        prompt_alias, model_alias, {"input": {"text": ""}}
    )

    mock_conversation_chain_predict.assert_called_with(input="Human: ")


@pytest.mark.parametrize(
    "prompt, model_alias, provider",
    [
        ("new prompt", "gpt-4", "openai"),
        ("new prompt", "meta.llama2-70b-chat-v1", "bedrock"),
    ],
)
@patch.object(LanguageModel, "get")
@patch.object(ConversationChain, "predict")
@patch.object(RedisCache, "__call__")
@patch.object(redis.connection.ConnectionPool, "get_connection")
@patch("botocore.session.Session")
def test_generate_from_prompt(
    mock_boto_session,
    mock_redis_get_connection,
    mock_redis_client,
    mock_conversation_chain_predict,
    mock_model_get,
    prompt,
    model_alias,
    provider,
):
    """Test generate from prompt template."""
    mock_redis_get_connection.return_value.retry.call_with_retry.return_value = dict()
    mock_conversation_chain_predict.return_value = dict()
    mock_model_get.return_value = LanguageModel(alias=model_alias, provider=provider)

    _ = F.generate_from_prompt(prompt, model_alias)

    mock_conversation_chain_predict.assert_called_with(input=prompt)
