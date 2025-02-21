"""Conftest."""

# Standard Library
import uuid
from typing import Optional

# 3rd party libraries
import pytest
from dyntastic import Dyntastic, Index
from moto import mock_aws  # Use mock_aws to mock all AWS services
from pydantic import Field

# Internal libraries
from onclusiveml.data.data_model.dynamodb import DynamoDBModel


@pytest.fixture(scope="session")
def TestDyntasticModel():
    """Fixture for the test Dyntastic model class."""

    class TestDyntasticModelInner(Dyntastic):
        """A minimal Dyntastic model for testing DynamoDBModel."""

        __table_name__ = "test_dynamodb_table"
        __hash_key__ = "id"
        __table_region__ = "us-east-1"
        id: str = Field(default_factory=lambda: str(uuid.uuid4()))
        name: str
        age: Optional[int] = None

    return TestDyntasticModelInner


@pytest.fixture(scope="function")
def dynamo_db_model(TestDyntasticModel):
    """Fixture to provide a DynamoDBModel instance with a mocked DynamoDB table."""
    with mock_aws():
        # Create the DynamoDB table using the Dyntastic model
        index = Index("name", index_name="name-index")

        TestDyntasticModel.create_table(index)
        # Return an instance of DynamoDBModel
        yield DynamoDBModel(model=TestDyntasticModel)


@pytest.fixture
def test_data(dynamo_db_model):
    """Sample data for testing."""
    items_data = [
        {"name": "Name1", "age": 25},
        {"name": "Name2", "age": 20},
        {"name": "Name2", "age": 26},
        {"name": "Name2", "age": 27},
        {"name": "Name2", "age": 35},
    ]
    for item_data in items_data:
        dynamo_db_model.create(item_data)
    return dynamo_db_model
