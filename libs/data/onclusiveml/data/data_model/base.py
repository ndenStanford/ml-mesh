"""Base Data Model."""

# Standard Library
from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Generic, List, Type, TypeVar

# 3rd party libraries
from pydantic import Field

# Internal libraries
from onclusiveml.core.serialization.schema import JsonApiSchema


T = TypeVar("T")


class BaseDataModel(JsonApiSchema, ABC, Generic[T]):
    """Abstract base class for data models.

    This class defines the interface for basic CRUD (Create, Read, Update, Delete)
    operations on a data store. It is designed to be subclassed by specific
    implementations for different types of data stores (e.g., databases, APIs).

    The class is generic over type T, which represents the type of items
    stored in the data model.
    """

    model: Type[T] = Field(...)

    def __init__(self, model: Type[T]):
        """Initialize the BaseDataModel with a specific model.

        Args:
            model (Type[T]): The model class representing the data schema.
        """
        super().__init__(model=model)

    @property
    @abstractmethod
    def table_name(self) -> str:
        """Abstract property to get the table name of the data model.

        Returns:
            str: The name of the table or data store.
        """

    @abstractmethod
    def get_all(self) -> List[T]:
        """Retrieve all items from the data store.

        Returns:
            List[T]: A list of all items in the data store.
        """

    @abstractmethod
    def get_one(self, id: str) -> T:
        """Retrieve a single item from the data store by its ID.

        Args:
            id (str): The unique identifier of the item to retrieve.

        Returns:
            T: The item with the specified ID, or None if not found.

        Raises:
            ItemNotFoundException: If the item does not exist.
            DataModelException: For other data-related errors.
        """

    @abstractmethod
    def create(self, item: Any) -> T:
        """Create a new item in the data store.

        Args:
            item (Any): The item to be created.

        Returns:
            T: The created item, potentially with additional metadata (e.g., ID).

        Raises:
            ValidationException: If the input data is invalid.
            DataModelException: For other data-related errors.
        """

    @abstractmethod
    def update(self, id: str, item: Any) -> T:
        """Update an existing item in the data store.

        Args:
            id (str): The unique identifier of the item to update.
            item (Any): The updated item data.

        Returns:
            T: The updated item, or None if the item with the given ID doesn't exist.

        Raises:
            ItemNotFoundException: If the item does not exist.
            ValidationException: If the input data is invalid.
            DataModelException: For other data-related errors.
        """

    @abstractmethod
    def get_query(self, query_profile: str, query_date: date) -> T:
        """Get result for a certain query.

        Args:
            query_profile (str): query string.
            query_date (date): Time for target query.

        Returns:
            T: The query related item, or None.

        Raises:
            QueryNotFoundException: If the query does not exist.
            ValidationException: If the query is invalid.
        """

    @abstractmethod
    def delete_one(self, id: str) -> T:
        """Delete a single item from the data store by its ID.

        Args:
            id (str): The unique identifier of the item to delete.

        Returns:
            T: The deleted item, or None if the item with the given ID doesn't exist.

        Raises:
            ItemNotFoundException: If the item does not exist.
            DataModelException: For other data-related errors.
        """

    @abstractmethod
    def delete_all(self) -> List[T]:
        """Delete all items from the data store.

        Returns:
            List[T]: A list of all deleted items.

        Raises:
            DataModelException: For errors during deletion.
        """
