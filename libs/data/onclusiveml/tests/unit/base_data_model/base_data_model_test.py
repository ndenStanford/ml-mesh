"""Test Base Data Model."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.data.data_model.base import BaseDataModel


def test_cannot_instantiate_base_class():
    """Test that BaseDataModel cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseDataModel()


def test_create_and_get_one_equality(data_model, item):
    """Test that created item can be retrieved and is equal to original."""
    data_model.create(item)
    retrieved_item = data_model.get_one(item.id)
    assert retrieved_item == item


def test_get_all_type(data_model, item, item2):
    """Test that get_all returns a list."""
    data_model.create(item)
    data_model.create(item2)
    all_items = data_model.get_all()
    assert isinstance(all_items, list)
    assert len(all_items) == 2


def test_get_all_contains_new_items(data_model, item, item2):
    """Test that get_all contains the first created item."""
    data_model.create(item)
    data_model.create(item2)
    all_items = data_model.get_all()
    assert item in all_items
    assert item2 in all_items


def test_update_equality(data_model, item, item_update):
    """Test that updated item is equal to the update data."""
    data_model.create(item)
    data_model.update(item.id, item_update)
    retrieved_item = data_model.get_one(item.id)
    assert retrieved_item == item_update


def test_delete_one_return_value(data_model, item):
    """Test that delete_one returns the deleted item."""
    data_model.create(item)
    deleted_item = data_model.delete_one(item.id)
    assert deleted_item == item


def test_delete_one_removes_item(data_model, item):
    """Test that delete_one actually removes the item."""
    data_model.create(item)
    data_model.delete_one(item.id)
    assert data_model.get_one(item.id) is None


def test_delete_all_return_count(data_model, item, item2):
    """Test that delete_all returns correct number of deleted items."""
    data_model.create(item)
    data_model.create(item2)
    deleted_items = data_model.delete_all()
    assert len(deleted_items) == 2


def test_delete_all_contains_first_item(data_model, item, item2):
    """Test that delete_all returns list containing first item."""
    data_model.create(item)
    data_model.create(item2)
    deleted_items = data_model.delete_all()
    assert item in deleted_items


def test_delete_all_contains_second_item(data_model, item, item2):
    """Test that delete_all returns list containing second item."""
    data_model.create(item)
    data_model.create(item2)
    deleted_items = data_model.delete_all()
    assert item2 in deleted_items


def test_delete_all_empties_data_model(data_model, item, item2):
    """Test that delete_all removes all items from data model."""
    data_model.create(item)
    data_model.create(item2)
    data_model.delete_all()
    assert data_model.get_all() == []


def test_get_table_name(data_model):
    """Test that get table name."""
    table_name = data_model.table_name
    assert isinstance(table_name, str)


def test_get_query(data_model, item, item2):
    """Test search query can  work."""
    data_model.create(item)
    data_model.create(item2)
    search_result = data_model.get_query("Item1")
    assert item in search_result
    assert item2 not in search_result
