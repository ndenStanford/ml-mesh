"""Test schemas."""

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
    schema = ModelSchema(model_name=model_name)

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
    schema = ModelSchema(model_name=model_name).save()

    schema_from_db = ModelSchema.get(schema.id)

    assert schema.id == schema_from_db.id
    assert schema.created_at == schema_from_db.created_at
    assert schema.model_name == schema_from_db.model_name


@pytest.mark.parametrize(
    "model_name, updated_model_name",
    [
        (
            "text-curie-008",
            "text-curie-009",
        )
    ],
)
def test_update(model_name, updated_model_name):
    """Test get item from table."""
    schema = ModelSchema(model_name=model_name).save()

    schema.update(model_name=updated_model_name)

    updated_schema = ModelSchema.get(schema.id)

    assert updated_schema.id == schema.id
    assert updated_schema.created_at == schema.created_at
    assert updated_schema.model_name == updated_model_name
    assert updated_schema.model_name != schema.model_name
