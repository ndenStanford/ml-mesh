"""Conftest."""

# 3rd party libraries
import pytest


@pytest.fixture
def url_model_namespace():
    """Create model namespace url."""
    return "http://backend:4000/api/v3/models/gpt-4o/generate?prompt=tell%20me%20a%20joke!!!"


@pytest.fixture
def url_model_namespace_async():
    """Create model namespace url."""
    return "http://backend:4000/api/v3/models/gpt-4o/generate/async?prompt=tell%20me%20a%20joke!!!"


@pytest.fixture
def url_generated_namespace():
    """Create generated namespace url."""
    return "http://backend:4000/api/v3/generated/"


@pytest.fixture
def url_model_namespace_status():
    """Create model status namespace url."""
    return "http://backend:4000/api/v3/models/status"


@pytest.fixture
def url_prompt_namespace():
    """Create prompt namespace url."""
    return "http://backend:4000/api/v3/prompts/english-summarization/generate/model/us.anthropic.claude-3-sonnet-20240229-v1:0"  # noqa: E501


@pytest.fixture
def url_prompt_namespace_async():
    """Create prompt namespace url."""
    return "http://backend:4000/api/v3/prompts/english-summarization/generate/async/model/us.anthropic.claude-3-sonnet-20240229-v1:0"  # noqa: E501


@pytest.fixture
def url_prompt_namespace_status():
    """Create prompts status namespace url."""
    return "http://backend:4000/api/v3/prompts/status"


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
