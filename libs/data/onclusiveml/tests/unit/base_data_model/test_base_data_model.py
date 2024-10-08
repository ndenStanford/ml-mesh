"""Test Base Data Model."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.data.data_model.base_data_model import BaseDataModel


def test_cannot_instantiate_base_class():
    """Test that BaseDataModel cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseDataModel()


def test_create(mock_data_model):
    """Test the _create method."""
    item = {"name": "Test Item"}
    created_item = mock_data_model._create(item)
    assert created_item == item
    assert mock_data_model._get_all() == [item]


def test_get_one(mock_data_model):
    """Test the _get_one method."""
    item = {"name": "Test Item"}
    mock_data_model._create(item)
    retrieved_item = mock_data_model._get_one("1")
    assert retrieved_item == item


def test_update(mock_data_model):
    """Test the _update method."""
    item = {"name": "Test Item"}
    mock_data_model._create(item)
    updated_item = {"name": "Updated Item"}
    result = mock_data_model._update("1", updated_item)
    assert result == updated_item
    assert mock_data_model._get_one("1") == updated_item


def test_delete_one(mock_data_model):
    """Test the _delete_one method."""
    item = {"name": "Test Item"}
    mock_data_model._create(item)
    deleted_item = mock_data_model._delete_one("1")
    assert deleted_item == item
    assert mock_data_model._get_one("1") is None


def test_delete_all(mock_data_model):
    """Test the _delete_all method."""
    items = [{"name": "Item 1"}, {"name": "Item 2"}]
    for item in items:
        mock_data_model._create(item)
    deleted_items = mock_data_model._delete_all()
    assert deleted_items == items
    assert mock_data_model._get_all() == []
