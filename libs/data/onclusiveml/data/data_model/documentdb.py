"""DocumentDB Data Model."""

# Standard Library
from typing import Any, Dict, List

# 3rd party libraries
from pydantic import BaseModel, Field

# Internal libraries
from onclusiveml.data.data_model.base import BaseDataModel
from onclusiveml.data.data_model.exception import (
    DataModelException,
    ItemNotFoundException,
    ValidationException,
)


class DocumentDBModel(BaseDataModel[Any]):
    """A data model class for interacting with DB tables.

    This class provides methods for CRUD operations on DB tables
    using the DocumentDB library for object mapping.
    """

    model: Any = Field(...)
    client: Any = Field(...)

    def __init__(self, model: Any, client: Any):
        """Initialize the BaseDataModel with a specific model.

        Args:
            model (Type[T]): The model class representing the data schema.
            client (Type[T]): The documentdb
            client.
        """
        super().__init__(model=model, client=client)

    @property
    def table_name(self) -> str:
        """Return the name of the DocumentDB table associated with the model.

        Returns:
            str: The name of the DocumentDB table.
        """
        return self.client._AbstractRepository__collection_name

    def get_all(self) -> List[BaseModel]:
        """Fetch all items from the DocumentDB table.

        Returns:
            List[T]: A list of all items in the table.

        Raises:
            DataModelException: If an error occurs while fetching items.
        """
        try:
            return list(self.client.find_by({}))
        except Exception as e:
            raise DataModelException(error=str(e)) from e

    def get_one(self, id: str) -> BaseModel:
        """Fetch a single item from the DocumentDB table by its ID.

        Args:
            id (str): The unique identifier of the item.

        Returns:
            BaseModel: The item with the specified ID.

        Raises:
            ItemNotFoundException: If the item does not exist.
            DataModelException: If an error occurs while fetching the item.
        """
        try:
            item = self.client.find_one_by_id(id)
        except Exception as e:
            raise DataModelException(error=str(e)) from e

        if item is None:
            raise ItemNotFoundException(item_id=id)

        return item

    def create(self, item: Dict[str, Any]) -> BaseModel:
        """Create a new item in the DocumentDB table.

        Args:
            item (Dict[str,Any]): The item data to create.

        Returns:
            BaseModel: The newly created item.

        Raises:
            ValidationException: If the input data is invalid.
            DataModelException: If an error occurs while creating the item.
        """
        try:
            new_item = self.model(**item)
            self.client.save(new_item)
            return new_item
        except ValueError as ve:
            raise ValidationException(error=str(ve)) from ve
        except Exception as e:
            raise DataModelException(error=str(e)) from e

    def update(self, id: str, item: Dict[str, Any]) -> BaseModel:
        """Update an existing item in the DocumentDB table.

        Args:
            id (str): The unique identifier of the item to update.
            item (Dict[str,Any]): The updated item data.

        Returns:
            BaseModel: The updated item.

        Raises:
            ItemNotFoundException: If the item does not exist.
            ValidationException: If the input data is invalid.
            DataModelException: If an error occurs while updating the item.
        """
        try:
            existing_item = self.client.find_one_by_id(id)
        except ValueError as ve:
            raise ValidationException(error=str(ve)) from ve
        except Exception as e:
            raise DataModelException(error=str(e)) from e

        if not existing_item:
            raise ItemNotFoundException(item_id=id)

        for key, value in item.items():
            setattr(existing_item, key, value)
        self.client.save(existing_item)

        return existing_item

    def get_query(self, search_query: dict) -> List[BaseModel]:
        """Get result for a certain DocumentDB search query.

        Args:
            search_query (str): serialized search query.

        Returns:
            T: The query related item, or None.

        Raises:
            ValidationException: If the query is invalid.
        """
        try:
            response = self.client.find_by(search_query)
            query_items = [item for item in response]
            return query_items
        except ValidationException as e:
            raise ValidationException("The search query format is invalid.") from e

    def delete_one(self, id: str) -> BaseModel:
        """Delete an item from the DocumentDB table by its ID.

        Args:
            id (str): The unique identifier of the item to delete.

        Returns:
            BaseModel: The deleted item.

        Raises:
            ItemNotFoundException: If the item does not exist.
            DataModelException: If an error occurs while deleting the item.
        """
        try:
            item = self.client.find_one_by_id(id)
            if item:
                self.client.delete(item)
                return item
        except Exception as e:
            raise DataModelException(error=str(e)) from e

        if not item:
            raise ItemNotFoundException(item_id=id)

    def delete_all(self) -> List[BaseModel]:
        """Delete all items in the DocumentDB table.

        Returns:
            List[T]: A list of all deleted items.

        Raises:
            DataModelException: If an error occurs while deleting items.
        """
        try:
            items = list(self.client.find_by({}))
            for item in items:
                self.client.delete(item)
            return items
        except Exception as e:
            raise DataModelException(error=str(e)) from e
