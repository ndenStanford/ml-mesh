"""Server test."""

# 3rd party libraries
from fastapi import FastAPI

# Source
from src.serve.server import get_model_server


def test_get_model_server():
    """Test get model server."""
    model_server = get_model_server()
    assert isinstance(model_server, FastAPI)
