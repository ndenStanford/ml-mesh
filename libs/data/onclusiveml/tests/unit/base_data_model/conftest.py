"""Conftest."""

# Standard Library
from typing import Type

# 3rd party libraries
import pytest
from pydantic import BaseModel, PrivateAttr

# Internal libraries
from onclusiveml.data.data_model.base import BaseDataModel


class Item(BaseModel):
    """Represents an item with an ID, name, and value."""

    id: str
    name: str
    value: int


class MockDataModel(BaseDataModel[Item]):
    """A mock implementation of BaseDataModel using an in-memory store."""

    _store: dict = PrivateAttr(default_factory=dict)

    def __init__(self, model: Type[Item]):
        """Initialise MockDataModel with specific model."""
        super().__init__(model=model)

    @property
    def table_name(self):
        """Return table name."""
        return "Mock table name"

    def get_all(self):
        """Retrieve all items from in-memory store."""
        return list(self._store.values())

    def get_one(self, id: str):
        """Retrieve a single item by id."""
        return self._store.get(id)

    def create(self, item: Item):
        """Create a new item in the in-memory store."""
        self._store[item.id] = item
        return item

    def update(self, id: str, item: Item):
        """Update an existing item in the in-memory store."""
        self._store[id] = item
        return item

    def delete_one(self, id: str):
        """Delete a single item by its id from in-memory store."""
        return self._store.pop(id, None)

    def delete_all(self):
        """Delete all items from in-memory store."""
        items = list(self._store.values())
        self._store.clear()
        return items

    def get_query(self, search_query: str):
        """Search the items satisfying given condition."""
        result = [
            item
            for item in self._store.values()
            if item.id == search_query or item.name == search_query
        ]
        return result


@pytest.fixture
def data_model():
    """Fixture for the data model."""
    return MockDataModel(model=Item)


@pytest.fixture
def item():
    """Fixture for a sample item."""
    return Item(id="1", name="Item1", value=100)


@pytest.fixture
def item_update():
    """Fixture for a sample item."""
    return Item(id="1", name="Item123", value=999)


@pytest.fixture
def item2():
    """Fixture for a second sample item."""
    return Item(id="2", name="Item2", value=200)
