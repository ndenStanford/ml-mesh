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
from src.prompt.schemas import PromptTemplateSchema
from src.prompt.tables import PromptTemplateTable
from src.settings import get_settings


settings = get_settings()

TEST_PROMPTS = [
    PromptTemplateSchema(template="template1", alias="t1"),
    PromptTemplateSchema(template="template2", alias="t2"),
    PromptTemplateSchema(template="template3", alias="t3"),
    PromptTemplateSchema(template="template4", alias="t4"),
]

TEST_MODELS = [
    ModelSchema(model_name="model-1", parameters=settings.OPENAI_PARAMETERS),
    ModelSchema(model_name="model-2", parameters=settings.OPENAI_PARAMETERS),
    ModelSchema(model_name="model-3", parameters=settings.OPENAI_PARAMETERS),
    ModelSchema(model_name="model-4", parameters=settings.OPENAI_PARAMETERS),
]


@pytest.fixture(scope="session")
def init_prompt_tables() -> Generator[None, None, None]:
    """Initializes dynamodb tables."""
    if not PromptTemplateTable.exists():
        PromptTemplateTable.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )
    yield
    PromptTemplateTable.delete_table()


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """Instanciates app."""
    # Source
    from src.app import app

    return app


@pytest.fixture(scope="session")
def init_model_tables() -> Generator[None, None, None]:  # noqa: F811
    """Initializes dynamodb tables."""
    if not ModelTable.exists():
        ModelTable.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )
    yield
    ModelTable.delete_table()


@pytest.fixture(scope="session")
def test_client(
    app: FastAPI, init_prompt_tables: Any, init_model_tables: Any
) -> Generator[TestClient, None, None]:
    """Instanciates test client."""
    yield TestClient(app=app)


@pytest.fixture(scope="module")
def create_prompts(test_client):
    """Create template for integration tests."""
    res = []
    for template in TEST_PROMPTS:
        res.append(template.save())
    return res


@pytest.fixture(scope="module")
def create_models(test_client):
    """Create model_name for integration tests."""
    res = []
    for model_name in TEST_MODELS:
        res.append(model_name.save())
    return res
