"""Test DynamoDB Data Model."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.data.data_model.exception import (
    ItemNotFoundException,
    ValidationException,
)


def test_create_item(dynamo_db_model):
    """Test creating an item."""
    item_data = {"name": "Alice", "age": 30}
    created_item = dynamo_db_model.create(item_data)
    assert created_item.name == "Alice"
    assert created_item.age == 30
    assert created_item.id is not None


def test_create_item_missing_required_field(dynamo_db_model):
    """Test creating an item without required fields."""
    item_data = {"age": 25}  # Missing 'name'
    with pytest.raises(ValidationException):
        dynamo_db_model.create(item_data)


def test_get_one_existing_item(dynamo_db_model):
    """Test retrieving an existing item."""
    # Create an item first
    item_data = {"name": "Bob", "age": 40}
    created_item = dynamo_db_model.create(item_data)
    # Retrieve the item
    retrieved_item = dynamo_db_model.get_one(created_item.id)
    assert retrieved_item is not None
    assert retrieved_item.name == "Bob"
    assert retrieved_item.age == 40


def test_get_one_nonexistent_item(dynamo_db_model):
    """Test retrieving a non-existent item."""
    with pytest.raises(ItemNotFoundException):
        retrieved_item = dynamo_db_model.get_one("nonexistent-id")  # noqa: F841


def test_get_all_items_names(dynamo_db_model):
    """Test retrieving all items and count."""
    items_data = [
        {"name": "Charlie", "age": 22},
        {"name": "Diana", "age": 28},
        {"name": "Eve", "age": 35},
    ]
    for item_data in items_data:
        dynamo_db_model.create(item_data)

    all_items = dynamo_db_model.get_all()
    names = [item.name for item in all_items]
    item_names_set = {item["name"] for item in items_data}
    assert set(names) == item_names_set


def test_get_all_items_type(dynamo_db_model):
    """Test retrieving all items type."""
    items_data = [
        {"name": "Charlie", "age": 22},
        {"name": "Diana", "age": 28},
        {"name": "Eve", "age": 35},
    ]
    for item_data in items_data:
        dynamo_db_model.create(item_data)

    all_items = dynamo_db_model.get_all()
    assert len(all_items) == 3
    assert isinstance(all_items, list)


def test_update_existing_item(dynamo_db_model):
    """Test updating an existing item."""
    # Create an item
    item_data = {"name": "Frank", "age": 45}
    created_item = dynamo_db_model.create(item_data)
    # Update the item
    updated_data = {"name": "Franklin", "age": 46}
    updated_item = dynamo_db_model.update(created_item.id, updated_data)
    assert updated_item is not None
    assert updated_item.name == "Franklin"
    assert updated_item.age == 46


def test_update_nonexistent_item(dynamo_db_model):
    """Test updating a non-existent item."""
    with pytest.raises(ItemNotFoundException):
        updated_data = {"name": "Grace", "age": 50}
        updated_item = dynamo_db_model.update(  # noqa: F841
            "nonexistent-id", updated_data
        )


def test_delete_existing_item(dynamo_db_model):
    """Test deleting an existing item."""
    # Create an item
    item_data = {"name": "Heidi", "age": 29}
    created_item = dynamo_db_model.create(item_data)
    # Delete the item
    deleted_item = dynamo_db_model.delete_one(created_item.id)
    assert deleted_item is not None
    assert deleted_item.name == "Heidi"
    # Verify the item is deleted
    with pytest.raises(ItemNotFoundException):
        retrieved_item = dynamo_db_model.get_one(created_item.id)  # noqa: F841


def test_delete_all_items_empty(dynamo_db_model):
    """Test deleting all items - check empty."""
    items_data = [
        {"name": "Ivan", "age": 31},
        {"name": "Judy", "age": 27},
    ]
    for item_data in items_data:
        dynamo_db_model.create(item_data)

    all_items = dynamo_db_model.get_all()
    assert len(all_items) == 2
    dynamo_db_model.delete_all()
    all_items = dynamo_db_model.get_all()
    assert len(all_items) == 0


def test_delete_nonexistent_item(dynamo_db_model):
    """Test deleting a non-existent item."""
    with pytest.raises(ItemNotFoundException):
        deleted_item = dynamo_db_model.delete_one("nonexistent-id")  # noqa: F841


def test_delete_all_items(dynamo_db_model):
    """Test deleting all items."""
    items_data = [
        {"name": "Ivan", "age": 31},
        {"name": "Judy", "age": 27},
    ]
    for item_data in items_data:
        dynamo_db_model.create(item_data)

    deleted_items = dynamo_db_model.delete_all()
    assert len(deleted_items) == 2
    # Verify all items are deleted
    all_items = dynamo_db_model.get_all()
    assert len(all_items) == 0


def test_create_item_with_additional_fields(dynamo_db_model):
    """Test creating an item with additional fields not defined in the model."""
    item_data = {"name": "Kevin", "age": 33, "extra_field": "should be ignored"}
    created_item = dynamo_db_model.create(item_data)
    assert created_item.name == "Kevin"
    assert created_item.age == 33
    assert not hasattr(created_item, "extra_field")


def test_update_item_with_partial_data(dynamo_db_model):
    """Test updating an item with partial data."""
    # Create an item
    item_data = {"name": "Laura", "age": 24}
    created_item = dynamo_db_model.create(item_data)
    # Update only the 'age' field
    updated_data = {"age": 25}
    updated_item = dynamo_db_model.update(created_item.id, updated_data)
    assert updated_item is not None
    assert updated_item.name == "Laura"  # Name should remain unchanged
    assert updated_item.age == 25


def test_get_dynamodb_table_name(dynamo_db_model):
    """Test get dynamodb table name."""
    table_name = dynamo_db_model.table_name
    assert isinstance(table_name, str)
