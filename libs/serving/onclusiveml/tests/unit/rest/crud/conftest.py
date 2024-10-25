"""Conftest."""

# Standard Library
import uuid
from typing import Optional

# 3rd party libraries
import pytest
from dyntastic import Dyntastic
from fastapi.testclient import TestClient
from moto import mock_aws  # Use mock_aws to mock all AWS services
from pydantic import Field

# Internal libraries
from onclusiveml.data.data_model.dynamodb import DynamoDBModel
from onclusiveml.serving.rest.crud._base import CRUDGenerator


@pytest.fixture(scope="session")
def TestDyntasticModel():
    """Fixture for the test Dyntastic model class."""

    class TestDyntasticModelInner(Dyntastic):
        """A minimal Dyntastic model for testing DynamoDBModel."""

        __table_name__ = "test_table_1"
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
        TestDyntasticModel.create_table()
        # Return an instance of DynamoDBModel
        yield DynamoDBModel(model=TestDyntasticModel)


@pytest.fixture(scope="function")
def app(dynamo_db_model, TestDyntasticModel):
    """Fixture to provide a FastAPI app with the CRUDRouter."""
    # 3rd party libraries
    from fastapi import FastAPI

    # Internal libraries
    from onclusiveml.core.base import (
        OnclusiveBaseModel,
        OnclusiveFrozenSettings,
    )

    class api_settings(OnclusiveFrozenSettings):
        model_name: str = "test-service"
        api_version: str = "v1"

    # Define the schema
    class ItemSchema(OnclusiveBaseModel):
        id: str = Field(default_factory=lambda: str(uuid.uuid4()))
        name: str
        age: Optional[int] = None

    class CreateItemSchema(OnclusiveBaseModel):
        name: str
        age: Optional[int] = None

    class UpdateItemSchema(OnclusiveBaseModel):
        name: Optional[str] = None
        age: Optional[int] = None

    # Create the FastAPI app
    app = FastAPI()
    # Include the router
    app.include_router(
        CRUDGenerator(
            schema=ItemSchema,
            create_schema=CreateItemSchema,
            update_schema=UpdateItemSchema,
            model=dynamo_db_model,
            api_settings=api_settings(),
            entity_name="test_table",
            tags=["Items"],
        )
    )

    return app


@pytest.fixture(scope="function")
def client(app):
    """Fixture to provide a TestClient for the FastAPI app."""
    with TestClient(app) as client:
        yield client
