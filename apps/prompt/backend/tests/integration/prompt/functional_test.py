"""Functional module tests."""

# 3rd party libraries
import pytest

# Source
from src.model.constants import ChatModel
from src.prompt import functional as F


@pytest.mark.parametrize(
    "model_alias, prompt",
    [
        (ChatModel.GPT3_5, "Hello"),
        (ChatModel.GPT4_TURBO, "This is an integration test."),
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
    "model_alias, prompt_alias",
    [
        (ChatModel.CLAUDE_2_1, "prompt1"),
        (ChatModel.GPT4_TURBO, "prompt2"),
    ],
)
@pytest.mark.order(11)
def test_generate_from_prompt_template(model_alias, prompt_alias, create_prompts, app):
    """Test generate prompt from template."""
    response = F.generate_from_prompt_template(prompt_alias, model_alias, **dict())
    assert isinstance(
        response,
        dict,
    )
    assert isinstance(response["generated"], str)


@pytest.mark.parametrize(
    "prompt_alias",
    [
        ("prompt1"),
        ("prompt2"),
    ],
)
@pytest.mark.order(12)
def test_generate_from_default_model(model_alias, prompt_alias, create_prompts, app):
    """Test generate prompt from template."""
    response = F.generate_from_default_model(prompt_alias, **dict())
    assert isinstance(
        response,
        dict,
    )
    assert isinstance(response["generated"], str)
