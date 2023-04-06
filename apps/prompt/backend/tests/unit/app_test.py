"""Test app."""

# 3rd party libraries
from fastapi import FastAPI

# Internal libraries
from onclusiveml.core.testing import get_override_settings_context_manager

# Source
from src.settings import get_settings


override_settings = get_override_settings_context_manager(get_settings)


def test_app_init(app):
    """Test app initialisation."""
    assert isinstance(app, FastAPI)


def test_app_attributes(app):
    """Test app attributes."""
    settings = get_settings()
    assert app.description == settings.API_DESCRIPTION
    assert app.docs_url == settings.DOCS_URL

    assert app.redoc_url == "/redoc"
    assert app.docs_url == "/docs"
    assert app.openapi_url == "/openapi.json"
    assert app.redoc_url == "/redoc"
