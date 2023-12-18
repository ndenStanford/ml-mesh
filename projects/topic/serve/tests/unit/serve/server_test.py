"""Server test."""

# 3rd party libraries
from fastapi import FastAPI

# Source
from src.serve.server import get_model_server


def test_get_model_server(artifacts):
    """Test get model server."""
    assert isinstance(get_model_server(artifacts), FastAPI)
