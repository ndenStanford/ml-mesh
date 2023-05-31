"""Test schemas."""

# Standard Library
# Standard library
import json

# 3rd party libraries
import pytest

# Source
from src.model.schemas import ModelSchema
from src.model.tables import ModelTable


@pytest.mark.parametrize(
    "model_name",
    [
        "text-curie-004",
        "text-curie-005",
    ],
)
def test_save(model_name):
    """Test save schema in db."""
    parameters = json.dumps(
        {
            "max_tokens": 10,
            "temperature": 0.3,
        }
    )
    schema = ModelSchema(model_name=model_name, parameters=parameters)

    saved_schema = schema.save()

    assert saved_schema.id is not None
    assert saved_schema.created_at is not None
    assert ModelTable.count() > 0


@pytest.mark.parametrize(
    "model_name",
    [
        "text-curie-006",
        "text-curie-007",
    ],
)
def test_get_exists(model_name):
    """Test get item from table."""
    parameters = json.dumps(
        {
            "max_tokens": 200,
            "temperature": 0.9,
        }
    )
    schema = ModelSchema(model_name=model_name, parameters=parameters).save()

    schema_from_db = ModelSchema.get(schema.model_name)

    assert schema.id == schema_from_db.id
    assert schema.created_at == schema_from_db.created_at
    assert schema.model_name == schema_from_db.model_name
    assert schema.parameters == schema_from_db.parameters


@pytest.mark.parametrize(
    "model_name, max_tokens, temperature",
    [
        (
            "model-x",
            100,
            0.1,
        ),
        (
            "model-y",
            312,
            0.4,
        ),
    ],
)
def test_get_models_different_params(model_name, max_tokens, temperature):
    """Test get item from table."""
    schema = ModelSchema(
        model_name=model_name,
        parameters=json.dumps({"max_tokens": max_tokens, "temperature": temperature}),
    ).save()

    schema_from_db = ModelSchema.get(schema.model_name)

    assert schema.id == schema_from_db.id
    assert schema.created_at == schema_from_db.created_at
    assert schema.model_name == model_name
    assert json.loads(schema.parameters)["max_tokens"] == max_tokens
    assert json.loads(schema.parameters)["temperature"] == temperature
