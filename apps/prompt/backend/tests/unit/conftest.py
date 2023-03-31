"""Conftest."""
from typing import Generator, Any

from src.prompt.tables import PromptTemplateTable
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient


@pytest.fixture(autouse=True)
def init_tables() -> Generator[None, None, None]:
    if not PromptTemplateTable.exists():
        PromptTemplateTable.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )
    yield
    PromptTemplateTable.delete_table()


@pytest.fixture
def app() -> FastAPI:
    from src.app import app

    return app


@pytest.fixture()
def client(app: FastAPI, init_tables: Any) -> Generator[TestClient, None, None]:
    yield TestClient(app=app)
