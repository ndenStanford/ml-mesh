"""Test DynamoDB Data Model."""

# 3rd party libraries
import pytest
from dyntastic.exceptions import DoesNotExist
from pydantic import ValidationError


def test_create_item(dynamo_db_model):
    """Test creating an item."""
    item_data = {"name": "Alice", "age": 30}
    created_item = dynamo_db_model._create(item_data)
    assert created_item.name == "Alice"
    assert created_item.age == 30
    assert created_item.id is not None


def test_create_item_missing_required_field(dynamo_db_model):
    """Test creating an item without required fields."""
    item_data = {"age": 25}  # Missing 'name'
    with pytest.raises(ValidationError):
        dynamo_db_model._create(item_data)


def test_get_one_existing_item(dynamo_db_model):
    """Test retrieving an existing item."""
    # Create an item first
    item_data = {"name": "Bob", "age": 40}
    created_item = dynamo_db_model._create(item_data)
    # Retrieve the item
    retrieved_item = dynamo_db_model._get_one(created_item.id)
    assert retrieved_item is not None
    assert retrieved_item.name == "Bob"
    assert retrieved_item.age == 40


def test_get_one_nonexistent_item(dynamo_db_model):
    """Test retrieving a non-existent item."""
    with pytest.raises(DoesNotExist):
        retrieved_item = dynamo_db_model._get_one("nonexistent-id")  # noqa: F841


def test_get_all_items(dynamo_db_model):
    """Test retrieving all items."""
    items_data = [
        {"name": "Charlie", "age": 22},
        {"name": "Diana", "age": 28},
        {"name": "Eve", "age": 35},
    ]
    for item_data in items_data:
        dynamo_db_model._create(item_data)

    all_items = dynamo_db_model._get_all()
    assert len(all_items) == 3
    names = [item.name for item in all_items]
    assert "Charlie" in names
    assert "Diana" in names
    assert "Eve" in names


def test_update_existing_item(dynamo_db_model):
    """Test updating an existing item."""
    # Create an item
    item_data = {"name": "Frank", "age": 45}
    created_item = dynamo_db_model._create(item_data)
    # Update the item
    updated_data = {"name": "Franklin", "age": 46}
    updated_item = dynamo_db_model._update(created_item.id, updated_data)
    assert updated_item is not None
    assert updated_item.name == "Franklin"
    assert updated_item.age == 46


def test_update_nonexistent_item(dynamo_db_model):
    """Test updating a non-existent item."""
    with pytest.raises(DoesNotExist):
        updated_data = {"name": "Grace", "age": 50}
        updated_item = dynamo_db_model._update(  # noqa: F841
            "nonexistent-id", updated_data
        )


def test_delete_existing_item(dynamo_db_model):
    """Test deleting an existing item."""
    # Create an item
    item_data = {"name": "Heidi", "age": 29}
    created_item = dynamo_db_model._create(item_data)
    # Delete the item
    deleted_item = dynamo_db_model._delete_one(created_item.id)
    assert deleted_item is not None
    assert deleted_item.name == "Heidi"
    # Verify the item is deleted
    with pytest.raises(DoesNotExist):
        retrieved_item = dynamo_db_model._get_one(created_item.id)  # noqa: F841


def test_delete_nonexistent_item(dynamo_db_model):
    """Test deleting a non-existent item."""
    with pytest.raises(DoesNotExist):
        deleted_item = dynamo_db_model._delete_one("nonexistent-id")  # noqa: F841


def test_delete_all_items(dynamo_db_model):
    """Test deleting all items."""
    items_data = [
        {"name": "Ivan", "age": 31},
        {"name": "Judy", "age": 27},
    ]
    for item_data in items_data:
        dynamo_db_model._create(item_data)

    deleted_items = dynamo_db_model._delete_all()
    assert len(deleted_items) == 2
    # Verify all items are deleted
    all_items = dynamo_db_model._get_all()
    assert len(all_items) == 0


def test_create_item_with_additional_fields(dynamo_db_model):
    """Test creating an item with additional fields not defined in the model."""
    item_data = {"name": "Kevin", "age": 33, "extra_field": "should be ignored"}
    created_item = dynamo_db_model._create(item_data)
    assert created_item.name == "Kevin"
    assert created_item.age == 33
    assert not hasattr(created_item, "extra_field")


def test_update_item_with_partial_data(dynamo_db_model):
    """Test updating an item with partial data."""
    # Create an item
    item_data = {"name": "Laura", "age": 24}
    created_item = dynamo_db_model._create(item_data)
    # Update only the 'age' field
    updated_data = {"age": 25}
    updated_item = dynamo_db_model._update(created_item.id, updated_data)
    assert updated_item is not None
    assert updated_item.name == "Laura"  # Name should remain unchanged
    assert updated_item.age == 25
