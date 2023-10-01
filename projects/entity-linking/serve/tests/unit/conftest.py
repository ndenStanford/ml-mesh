"""Conftest."""

# Standard Library
from typing import Generator

# 3rd party libraries
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

# Source
from src.serve.model import EntityLinkingServedModel
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture(scope="function")
def entity_linking_model(settings) -> FastAPI:
    """App fixture."""
    # Source
    return EntityLinkingServedModel(name=settings.model_name)


@pytest.fixture(scope="function")
def model_server(settings, entity_linking_model) -> FastAPI:
    """Server fixture."""
    return ModelServer(configuration=settings, model=entity_linking_model)


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
