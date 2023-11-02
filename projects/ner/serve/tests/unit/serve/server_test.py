"""Server test."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
from fastapi import FastAPI


@patch("json.loads")
@patch("builtins.open")
def test_get_model_server(mock_open, mock_json):
    """Test get model server."""
    # Source
    from src.serve.__main__ import get_model_server

    model_server = get_model_server()

    assert isinstance(model_server, FastAPI)
