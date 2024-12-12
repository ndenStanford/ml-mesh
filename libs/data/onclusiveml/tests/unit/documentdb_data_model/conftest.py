"""Conftest."""

# Standard Library
from typing import Optional

# 3rd party libraries
import mongomock
import pytest
from pydantic import BaseModel
from pydantic_mongo import PydanticObjectId

# Internal libraries
from onclusiveml.data.data_model.documentdb import DocumentDBModel


@pytest.fixture(scope="function")
def TestDocumentDBClient():
    """Mock DocumentDB client."""
    return mongomock.MongoClient()


@pytest.fixture(scope="function")
def TestDocumentDBModel():
    """A minimal DocumentDB model for testing DocumentDBModel."""

    class TestDocumentDBModelInner(BaseModel):
        """A minimal DocumentDB model for testing DocumentDBModel."""

        id: Optional[PydanticObjectId] = None
        name: str
        age: Optional[int] = None

    return TestDocumentDBModelInner


@pytest.fixture(scope="function")
def document_db_model(TestDocumentDBClient, TestDocumentDBModel):
    """Fixture to provide a DynamoDBModel instance with a mocked DynamoDB table."""
    document_db_model = DocumentDBModel(
        TestDocumentDBClient,
        TestDocumentDBModel,
        "test_documentdb_database_name",
        "test_documentdb_collection_name",
        True,
    )
    yield document_db_model


@pytest.fixture
def test_data(document_db_model):
    """Sample data for testing."""
    items_data = [
        {"name": "Name1", "age": 25},
        {"name": "Name2", "age": 20},
        {"name": "Name2", "age": 26},
        {"name": "Name2", "age": 27},
        {"name": "Name2", "age": 35},
    ]
    for item_data in items_data:
        document_db_model.create(item_data)
    return document_db_model
