"""Conftest."""

# 3rd party libraries
import pytest
from requests_toolbelt.sessions import BaseUrlSession

# Source
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture
def test_client(settings):
    """Client-like session with base url to avoid duplication.

    Reference:
        https://toolbelt.readthedocs.io/en/latest/sessions.html#baseurlsession
    """
    test_model_server_url = f"http://serve:{settings.uvicorn_settings.port}"

    return BaseUrlSession(base_url=test_model_server_url)
