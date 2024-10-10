"""DynamoDB Data Model."""

# Standard Library
from typing import List, Type, TypeVar

# 3rd party libraries
from dyntastic import Dyntastic
from pydantic import Field

# Internal libraries
from onclusiveml.data.data_model.base import BaseDataModel


T = TypeVar("T", bound=Dyntastic)


class DynamoDBModel(BaseDataModel[T]):
    """A data model class for interacting with DynamoDB tables.

    This class provides methods for CRUD operations on DynamoDB tables
    using the Dyntastic library for object mapping.
    """

    model: Type[T] = Field(...)

    def __init__(self, model: Type[T]):
        """Initialize the DynamoDBModel with a specific Dyntastic model.

        Args:
            model (Type[T]): The Dyntastic model class for the DynamoDB table.
        """
        super().__init__(model=model)

    def _get_all(self) -> List[T]:
        """Fetch all items from the DynamoDB table.

        Returns:
            List[T]: A list of all items in the table.
        """
        return list(self.model.scan())

    def _get_one(self, id: str) -> T:
        """Fetch a single item from the DynamoDB table by its ID.

        Args:
            id (str): The unique identifier of the item.

        Returns:
            T: The item with the specified ID, or None if not found.
        """
        return self.model.get(id)

    def _create(self, item: T) -> T:
        """Create a new item in the DynamoDB table.

        Args:
            item (T): The item to be created.

        Returns:
            T: The newly created item.
        """
        new_item = self.model(**item)
        new_item.save()
        return new_item

    def _update(self, id: str, item: T) -> T:
        """Update an existing item in the DynamoDB table.

        Args:
            id (str): The unique identifier of the item to update.
            item (T): The updated item data.

        Returns:
            T: The updated item, or None if the item with the given ID doesn't exist.
        """
        existing_item = self.model.get(id)
        if not existing_item:
            return None
        for key, value in item.items():
            setattr(existing_item, key, value)
        existing_item.save()
        return existing_item

    def _delete_one(self, id: str) -> T:
        """Delete an item from the DynamoDB table by its ID.

        Args:
            id (str): The unique identifier of the item to delete.

        Returns:
            T: The deleted item, or None if the item with the given ID doesn't exist.
        """
        item = self.model.get(id)
        if item:
            item.delete()
            return item
        return None

    def _delete_all(self) -> List[T]:
        """Delete all items in the DynamoDB table.

        Returns:
            List[T]: A list of all deleted items.
        """
        items = list(self.model.scan())
        for item in items:
            item.delete()
        return items
