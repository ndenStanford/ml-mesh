"""Conftest."""

# Standard Library
from typing import Generator

# 3rd party libraries
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient


@pytest.fixture
def app() -> FastAPI:
    """App fixture."""
    # Source
    from src.app import app

    return app


@pytest.fixture()
def test_client(app: FastAPI) -> Generator[TestClient, None, None]:
    """Test client fixture."""
    yield TestClient(app=app)


@pytest.fixture
def example_content_input() -> str:
    """Example content input fixture."""
    content = "I love living in England. London is a wonderful city."
    return content


@pytest.fixture
def example_entities_input() -> str:
    """Entities input fixture."""
    entities = [{"text": "England"}, {"text": "London"}]
    return entities


@pytest.fixture
def example_entities_output() -> str:
    """Entities output fixture."""
    entities = [
        {"text": "England", "wiki_link": "https://www.wikidata.org/wiki/Q21"},
        {"text": "London", "wiki_link": "https://www.wikidata.org/wiki/Q84"},
    ]
    return entities
