"""Conftest."""

# Standard Library
import os
import uuid
from typing import List, Optional

# 3rd party libraries
import pytest
from bson import ObjectId
from dyntastic import Dyntastic, Index
from moto import mock_aws  # Use mock_aws to mock all AWS services
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, PydanticObjectId
from pymongo import MongoClient

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.data.data_model.documentdb import DocumentDBModel


# # --- settings classes
# @pytest.fixture(scope="session")
# def ConnectionSettings():

#     class ConnectionSettingsInner(OnclusiveBaseSettings):
#         """Tracked NER model specs."""

#         username: str = "mladmin"
#         password: str = "kjsuavzg"
#         endpoint: str = "onclusiveml-cluster-dev.cluster-c7sisgss8ghm.us-east-2.docdb.amazonaws.com"
#         port: int = 27017
#         ca_file_path: str = "global-bundle.pem"
#         database_name: str = "example"

#     return ConnectionSettingsInner


# @pytest.fixture(scope="session")
# def TestDocumentDBModel(ConnectionSettings):
#     """Fixture for the test Dyntastic model class."""

#     settings = ConnectionSettings()

#     class TestModel(BaseModel):
#         """A minimal Dyntastic model for testing DynamoDBModel."""

#         id: Optional[PydanticObjectId] = None
#         name: str
#         age: Optional[int] = None

#     class TestDocumentDBModelInner(AbstractRepository[TestModel]):
#         class Meta:
#             collection_name = "test_documentdb_table"

#     # Create the MongoDB client connection string
#     connection_string = (
#         f"mongodb://{settings.username}:{settings.password}@{settings.endpoint}:{settings.port}/"
#         f"?tls=true&tlsCAFile={settings.ca_file_path}&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
#     )

#     # Connect to Amazon DocumentDB
#     client = MongoClient(connection_string)
#     print("Client connected:", client)

#     database = client["example"]

#     model = TestDocumentDBModelInner(database=database)

#     return model


@pytest.fixture(scope="session")
def TestDocumentDBModel():
    class TestDocumentDBModelInner(BaseModel):
        """A minimal Dyntastic model for testing DynamoDBModel."""

        id: Optional[PydanticObjectId] = None
        name: str
        age: Optional[int] = None

    return TestDocumentDBModelInner


@pytest.fixture(scope="function")
def document_db_model(TestDocumentDBModel):
    """Fixture to provide a DynamoDBModel instance with a mocked DynamoDB table."""
    document_db_model = DocumentDBModel(
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
