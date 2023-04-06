"""Test helper."""

# Standard Library
import asyncio

# 3rd party libraries
import pytest
from fastapi import HTTPException

# Internal libraries
from onclusiveml.core.testing import get_override_settings_context_manager

# Source
from src.helpers import api_key_header_auth
from src.settings import get_settings


override_settings = get_override_settings_context_manager(get_settings)


def test_api_key_header_auth():
    """Test API key auth header."""
    settings = get_settings()
    assert api_key_header_auth.scheme_name == "APIKeyHeader"
    assert api_key_header_auth.auto_error is True
    assert api_key_header_auth.model.name == settings.API_KEY_NAME


@override_settings(API_KEY="123456")
def test_get_api_key():
    """Test API key."""
    _ = get_settings()
    # Source
    from src.helpers import get_api_key

    asyncio.run(get_api_key(api_key_header="123456"))


@override_settings(API_KEY="123456")
def test_get_api_key_fail():
    """Test API key."""
    _ = get_settings()
    # Source
    from src.helpers import get_api_key

    with pytest.raises(HTTPException):
        asyncio.run(get_api_key(api_key_header="abcd"))


ß
