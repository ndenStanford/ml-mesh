"""Conftest."""

# Standard Library
from typing import Any, Generator

# 3rd party libraries
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

# Source
from src.model.schemas import ModelSchema
from src.model.tables import ModelTable


TEST_MODELS = [
    ModelSchema(model_name="model-1"),
    ModelSchema(model_name="model-2"),
    ModelSchema(model_name="model-3"),
    ModelSchema(model_name="model-4"),
]


@pytest.fixture(autouse=True)
def init_tables() -> Generator[None, None, None]:
    """Initializes dynamodb tables."""
    if not ModelTable.exists():
        ModelTable.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )
    yield
    ModelTable.delete_table()


@pytest.fixture
def app() -> FastAPI:
    """Instanciates app."""
    # Source
    from src.app import app

    return app


@pytest.fixture()
def test_client(app: FastAPI, init_tables: Any) -> Generator[TestClient, None, None]:
    """instanciates test client."""
    yield TestClient(app=app)


@pytest.fixture()
def create_models(init_tables):
    """Create model_name for integration tests."""
    res = []
    for model_name in TEST_MODELS:
        res.append(model_name.save())
    return res
