"""Base Data Model."""

# Standard Library
from abc import ABC, abstractmethod
from typing import Any, Generic, List, TypeVar

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel


T = TypeVar("T")


class BaseDataModel(OnclusiveBaseModel, ABC, Generic[T]):
    """Abstract base class for data models.

    This class defines the interface for basic CRUD (Create, Read, Update, Delete)
    operations on a data store. It is designed to be subclassed by specific
    implementations for different types of data stores (e.g., databases, APIs).

    The class is generic over type T, which represents the type of items
    stored in the data model.
    """

    @abstractmethod
    def _get_all(self) -> List[Any]:
        """Retrieve all items from the data store.

        Returns:
            List[Any]: A list of all items in the data store.
        """
        pass

    @abstractmethod
    def _get_one(self, id: str) -> Any:
        """Retrieve a single item from the data store by its ID.

        Args:
            id (str): The unique identifier of the item to retrieve.

        Returns:
            Any: The item with the specified ID, or None if not found.

        Raises:
            ItemNotFoundException: If the item does not exist.
            DataModelException: For other data-related errors.
        """
        pass

    @abstractmethod
    def _create(self, item: Any) -> Any:
        """Create a new item in the data store.

        Args:
            item (Any): The item to be created.

        Returns:
            Any: The created item, potentially with additional metadata (e.g., ID).

        Raises:
            ValidationException: If the input data is invalid.
            DataModelException: For other data-related errors.
        """
        pass

    @abstractmethod
    def _update(self, id: str, item: Any) -> Any:
        """Update an existing item in the data store.

        Args:
            id (str): The unique identifier of the item to update.
            item (Any): The updated item data.

        Returns:
            Any: The updated item, or None if the item with the given ID doesn't exist.

        Raises:
            ItemNotFoundException: If the item does not exist.
            ValidationException: If the input data is invalid.
            DataModelException: For other data-related errors.
        """
        pass

    @abstractmethod
    def _delete_one(self, id: str) -> Any:
        """Delete a single item from the data store by its ID.

        Args:
            id (str): The unique identifier of the item to delete.

        Returns:
            Any: The deleted item, or None if the item with the given ID doesn't exist.

        Raises:
            ItemNotFoundException: If the item does not exist.
            DataModelException: For other data-related errors.
        """
        pass

    @abstractmethod
    def _delete_all(self) -> List[Any]:
        """Delete all items from the data store.

        Returns:
            List[Any]: A list of all deleted items.

        Raises:
            DataModelException: For errors during deletion.
        """
        pass
