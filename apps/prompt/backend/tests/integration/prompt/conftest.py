"""Conftest."""

# Standard Library
from typing import Any, Generator

# 3rd party libraries
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

# Source
from src.prompt.schemas import PromptTemplateSchema
from src.prompt.tables import PromptTemplateTable


TEST_PROMPTS = [
    PromptTemplateSchema(template="template1"),
    PromptTemplateSchema(template="template2"),
    PromptTemplateSchema(template="template3"),
    PromptTemplateSchema(template="template4"),
]


@pytest.fixture(autouse=True)
def init_tables() -> Generator[None, None, None]:
    """Initializes dynamodb tables."""
    if not PromptTemplateTable.exists():
        PromptTemplateTable.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )
    yield
    PromptTemplateTable.delete_table()


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
def create_prompts(init_tables):
    """Create template for integration tests."""
    res = []
    for template in TEST_PROMPTS:
        res.append(template.save())
    return res
