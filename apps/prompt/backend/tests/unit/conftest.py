"""Conftest."""

# Standard Library
from typing import Generator

# 3rd party libraries
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient


@pytest.fixture
def app() -> FastAPI:
    # Source
    from src.app import app

    return app


@pytest.fixture()
def test_client(app: FastAPI) -> Generator[TestClient, None, None]:
    yield TestClient(app=app)
