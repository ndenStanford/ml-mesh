"""Conftest."""

# Standard Library
import logging
from typing import Generator

# 3rd party libraries
import pytest
from fastapi import FastAPI
from github.GithubException import UnknownObjectException
from starlette.testclient import TestClient

# Source
from src._init import init
from src.project.tables import Project
from src.prompt.tables import PromptTemplate
from src.settings import get_settings


settings = get_settings()


TEST_PROJECTS = [
    Project(alias="integration-test-1"),
    Project(alias="integration-test-2"),
]


TEST_PROMPTS = [
    PromptTemplate(alias="prompt1", template="template1", project="integration-test-1"),
    PromptTemplate(alias="prompt2", template="template2", project="integration-test-2"),
    PromptTemplate(alias="prompt3", template="template3", project="integration-test-2"),
]


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """Instanciates app."""
    # Source
    from src.app import app

    init()
    return app


@pytest.fixture(scope="session")
def test_client(app: FastAPI) -> Generator[TestClient, None, None]:
    """Instanciates test client."""
    yield TestClient(app=app)


@pytest.fixture(scope="session")
def create_projects(test_client):
    """Create template for integration tests."""
    res = []
    for project in TEST_PROJECTS:
        res.append(project.save())
    return res


@pytest.fixture(scope="session")
def create_prompts(create_projects, test_client):
    """Create template for integration tests."""
    res = []
    for template in TEST_PROMPTS:
        res.append(template.save())
    return res


def pytest_sessionfinish(session, exitstatus):
    """Cleanup tests."""
    for template in TEST_PROMPTS:
        try:
            template.delete()
        except UnknownObjectException:
            logging.info("path does not exist.")
    for project in TEST_PROJECTS:
        try:
            project.delete()
        except UnknownObjectException:
            logging.info("path does not exist.")
