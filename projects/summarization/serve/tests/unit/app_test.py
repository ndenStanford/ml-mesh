"""Test app."""

# 3rd party libraries
from fastapi import FastAPI

# Source
from src.app import settings


def test_app_init(app):
    """Test app initialisation."""
    assert isinstance(app, FastAPI)


def test_app_attributes(app):
    """Test app attributes."""
    assert app.description == settings.API_DESCRIPTION
    assert app.docs_url == settings.DOCS_URL
