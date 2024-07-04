"""Conftest."""

# 3rd party libraries
import pytest


@pytest.fixture
def url_model_namespace():
    """Create model namespace url."""
    return "http://backend:4000/api/v2/models/gpt-4/generate?prompt=tell%20me%20a%20joke!!!"


@pytest.fixture
def url_prompt_namespace():
    """Create prompt namespace url."""
    return "http://backend:4000/api/v2/ \
        prompts/english-summarization/generate/model/anthropic.claude-3-sonnet-20240229-v1:0"


@pytest.fixture
def headers():
    """Create headers."""
    return {
        "accept": "application/json",
        "Content-Type": "application/json",
    }


@pytest.fixture
def payload():
    """Create payload."""
    return {"input": {"number": 5, "text": "what is the capital of US??"}}
