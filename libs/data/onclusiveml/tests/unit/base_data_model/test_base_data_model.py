"""Test Base Data Model."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.data.data_model.base import BaseDataModel


def test_cannot_instantiate_base_class():
    """Test that BaseDataModel cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseDataModel()


def test_create_and_get_one(data_model, item):
    """Test create and get one function."""
    data_model.create(item)
    retrieved_item = data_model.get_one(item.id)
    assert retrieved_item == item


def test_get_all(data_model, item, item2):
    """Test get all function."""
    data_model.create(item)
    data_model.create(item2)
    all_items = data_model.get_all()
    assert len(all_items) == 2
    assert item in all_items
    assert item2 in all_items


def test_update(data_model, item, item_update):
    """Test update function."""
    data_model.create(item)
    data_model.update(item.id, item_update)
    retrieved_item = data_model.get_one(item.id)
    assert retrieved_item == item_update


def test_delete_one(data_model, item):
    """Test delete one function."""
    data_model.create(item)
    deleted_item = data_model.delete_one(item.id)
    assert deleted_item == item
    assert data_model.get_one(item.id) is None


def test_delete_all(data_model, item, item2):
    """Test delete all function."""
    data_model.create(item)
    data_model.create(item2)
    deleted_items = data_model.delete_all()
    assert len(deleted_items) == 2
    assert item in deleted_items
    assert item2 in deleted_items
    assert data_model.get_all() == []
