"""Functional module tests."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
import redis
from langchain.chains import ConversationChain
from langchain_core.runnables.base import RunnableSequence
from redis_cache import RedisCache

# Source
from src.model.tables import LanguageModel
from src.prompt import functional as F
from src.prompt.tables import PromptTemplate


@pytest.mark.parametrize(
    "project, prompt_alias, template, text, model_alias, provider",
    [
        ("new-project1", "prompt-1", "{text}", "hello", "gpt-4o", "openai"),
        (
            "new-project2",
            "prompt-2",
            "{text}",
            "good bye",
            "meta.llama2-70b-chat-v1",
            "bedrock",
        ),
    ],
)
@patch.object(PromptTemplate, "get")
@patch.object(LanguageModel, "get")
@patch.object(RunnableSequence, "invoke")
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
    text,
    model_alias,
    provider,
):
    """Test generate from prompt template."""
    prompt = PromptTemplate(alias=prompt_alias, template=template, project=project)
    mock_redis_get_connection.return_value.retry.call_with_retry.return_value = dict()
    mock_conversation_chain_predict.return_value = dict()
    mock_model_get.return_value = LanguageModel(alias=model_alias, provider=provider)
    mock_prompt_get.return_value = prompt

    _ = F.generate_from_prompt_template(
        prompt_alias, model_alias, **{"input": {"text": text}}
    )

    mock_conversation_chain_predict.assert_called_with(
        {"text": text, "format_instructions": prompt.format_instructions}
    )


@pytest.mark.parametrize(
    "prompt, model_alias, provider",
    [
        ("Hello there", "gpt-4o", "openai"),
        ("Good evening", "meta.llama2-70b-chat-v1", "bedrock"),
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


@pytest.mark.parametrize(
    "project, prompt_alias, template, text, model_alias,provider",
    [
        (
            "new-project1",
            "english-summarization",
            "What is the capital of {text}",
            "Turkey",
            "gpt-4o",
            "openai",
        ),
        (
            "new-project1",
            "prompt-b",
            "My favourite film is {text}",
            "Starship Troopers",
            "us.anthropic.claude-3-haiku-20240307-v1:0",
            "openai",
        ),
    ],
)
@patch.object(PromptTemplate, "get")
@patch.object(LanguageModel, "get")
@patch.object(RunnableSequence, "invoke")
@patch.object(RedisCache, "__call__")
@patch.object(redis.connection.ConnectionPool, "get_connection")
@patch("botocore.session.Session")
def test_generate_from_prompt_default_model(
    mock_boto_session,
    mock_redis_get_connection,
    mock_redis_client,
    mock_conversation_chain_predict,
    mock_model_get,
    mock_prompt_get,
    project,
    prompt_alias,
    template,
    text,
    model_alias,
    provider,
):
    """Test generate from prompt template default models."""
    prompt = PromptTemplate(alias=prompt_alias, template=template, project=project)
    mock_redis_get_connection.return_value.retry.call_with_retry.return_value = dict()
    mock_conversation_chain_predict.return_value = dict()
    mock_model_get.return_value = LanguageModel(alias=model_alias, provider=provider)
    mock_prompt_get.return_value = prompt

    _ = F.generate_from_default_model(prompt_alias, **{"input": {"text": text}})

    mock_conversation_chain_predict.assert_called_with(
        {"text": text, "format_instructions": prompt.format_instructions}
    )
