"""Functional module tests."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
from langchain_core.runnables.base import RunnableSequence

# Source
from src.model.constants import ChatModel
from src.prompt import functional as F


@pytest.mark.parametrize(
    "model_alias, prompt",
    [
        (ChatModel.GPT4_O_MINI, "Hello"),
        (ChatModel.GPT4_O, "This is an integration test."),
    ],
)
@pytest.mark.order(10)
def test_generate_from_prompt(model_alias, prompt, app):
    """Test generate from prompt."""
    response = F.generate_from_prompt(prompt, model_alias)

    assert isinstance(
        response,
        str,
    )

    assert isinstance(response, str)


@pytest.mark.parametrize(
    "model_alias, prompt_alias, payload",
    [
        (ChatModel.CLAUDE_2_1, "prompt1", {}),
        (ChatModel.GPT4_O, "prompt2", {}),
        (ChatModel.GPT4_O, "prompt3", {"input": {"country": "Norway"}}),
    ],
)
@pytest.mark.order(11)
def test_generate_from_prompt_template(
    model_alias, prompt_alias, payload, create_prompts, app
):
    """Test generate prompt from template."""
    response = F.generate_from_prompt_template(prompt_alias, model_alias, **payload)
    assert isinstance(
        response,
        dict,
    )
    assert isinstance(response["generated"], str)


@pytest.mark.parametrize(
    "model_alias, prompt_alias, payload, result",
    [
        (
            ChatModel.GPT4_O,
            "prompt3",
            {
                "input": {"country": "England"},
                "output": {"capital": "capital of country"},
                "str_output_parser": True,
            },
            {"capital": "London"},
        ),
    ],
)
@patch.object(RunnableSequence, "invoke")
@pytest.mark.order(13)
def test_generate_from_prompt_template_json_build(
    mock_runnable_sequence_invoke,
    model_alias,
    prompt_alias,
    payload,
    result,
    create_prompts,
    app,
):
    """Test generate prompt from template."""
    # Set side_effect before calling the function
    mock_runnable_sequence_invoke.side_effect = [
        Exception("Test exception"),
        str(result),
    ]

    response = F.generate_from_prompt_template(prompt_alias, model_alias, **payload)
    # assert that final response is equal to expected response
    assert response == result


@pytest.mark.parametrize(
    "prompt_alias, payload",
    [
        ("prompt1", {}),
        ("prompt2", {}),
        ("prompt3", {"input": {"country": "Norway"}}),
    ],
)
@pytest.mark.order(12)
def test_generate_from_default_model(prompt_alias, payload, create_prompts, app):
    """Test generate prompt from template."""
    response = F.generate_from_default_model(prompt_alias, **payload)
    assert isinstance(
        response,
        dict,
    )
    assert isinstance(response["generated"], str)
