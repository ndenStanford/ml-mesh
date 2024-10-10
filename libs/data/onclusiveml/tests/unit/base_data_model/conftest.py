"""Conftest."""

# Standard Library
from typing import Any, Dict, List

# 3rd party libraries
import pytest
from pydantic import PrivateAttr

# Internal libraries
from onclusiveml.data.data_model.base import BaseDataModel


class MockDataModel(BaseDataModel[Any]):
    """An implementation of BaseDataModel for testing."""

    _data_store: Dict[str, Any] = PrivateAttr(default_factory=dict)

    def _get_all(self) -> List[Any]:
        return list(self._data_store.values())

    def _get_one(self, id: str) -> Any:
        return self._data_store.get(id)

    def _create(self, item: Any) -> Any:
        id = str(len(self._data_store) + 1)
        self._data_store[id] = item
        return item

    def _update(self, id: str, item: Any) -> Any:
        if id in self._data_store:
            self._data_store[id] = item
            return item
        return None

    def _delete_one(self, id: str) -> Any:
        return self._data_store.pop(id, None)

    def _delete_all(self) -> List[Any]:
        deleted_items = list(self._data_store.values())
        self._data_store.clear()
        return deleted_items


@pytest.fixture
def mock_data_model() -> MockDataModel:
    """Fixture for the MockDataModel instance."""
    return MockDataModel()
