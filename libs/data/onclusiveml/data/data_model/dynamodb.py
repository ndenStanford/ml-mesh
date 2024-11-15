"""DynamoDB Data Model."""

# Standard Library
from typing import Any, Dict, List

# 3rd party libraries
from dyntastic import Dyntastic
from dyntastic.exceptions import DoesNotExist

# Internal libraries
from onclusiveml.data.data_model.base import BaseDataModel
from onclusiveml.data.data_model.exception import (
    DataModelException,
    ItemNotFoundException,
    ValidationException,
)


class DynamoDBModel(BaseDataModel[Dyntastic]):
    """A data model class for interacting with DynamoDB tables.

    This class provides methods for CRUD operations on DynamoDB tables
    using the Dyntastic library for object mapping.
    """

    @property
    def table_name(self) -> str:
        """Return the name of the DynamoDB table associated with the model.

        Returns:
            str: The name of the DynamoDB table.
        """
        return self.model.__table_name__

    def get_all(self) -> List[Dyntastic]:
        """Fetch all items from the DynamoDB table.

        Returns:
            List[T]: A list of all items in the table.

        Raises:
            DataModelException: If an error occurs while fetching items.
        """
        try:
            return list(self.model.scan())
        except Exception as e:
            raise DataModelException(error=str(e)) from e

    def get_one(self, id: str) -> Dyntastic:
        """Fetch a single item from the DynamoDB table by its ID.

        Args:
            id (str): The unique identifier of the item.

        Returns:
            Dyntastic: The item with the specified ID.

        Raises:
            ItemNotFoundException: If the item does not exist.
            DataModelException: If an error occurs while fetching the item.
        """
        try:
            item = self.model.get(id)
            if item is None:
                raise ItemNotFoundException(item_id=id)
            return item
        except DoesNotExist:
            raise ItemNotFoundException(item_id=id)
        except Exception as e:
            raise DataModelException(error=str(e)) from e

    def create(self, item: Dict[str, Any]) -> Dyntastic:
        """Create a new item in the DynamoDB table.

        Args:
            item (Dict[str,Any]): The item data to create.

        Returns:
            Dyntastic: The newly created item.

        Raises:
            ValidationException: If the input data is invalid.
            DataModelException: If an error occurs while creating the item.
        """
        try:
            new_item = self.model(**item)
            new_item.save()
            return new_item
        except ValueError as ve:
            raise ValidationException(error=str(ve)) from ve
        except Exception as e:
            raise DataModelException(error=str(e)) from e

    def update(self, id: str, item: Dict[str, Any]) -> Dyntastic:
        """Update an existing item in the DynamoDB table.

        Args:
            id (str): The unique identifier of the item to update.
            item (Dict[str,Any]): The updated item data.

        Returns:
            Dyntastic: The updated item.

        Raises:
            ItemNotFoundException: If the item does not exist.
            ValidationException: If the input data is invalid.
            DataModelException: If an error occurs while updating the item.
        """
        try:
            existing_item = self.model.get(id)
            if not existing_item:
                raise ItemNotFoundException(item_id=id)
            for key, value in item.items():
                setattr(existing_item, key, value)
            existing_item.save()
            return existing_item
        except DoesNotExist:
            raise ItemNotFoundException(item_id=id)
        except ValueError as ve:
            raise ValidationException(error=str(ve)) from ve
        except Exception as e:
            raise DataModelException(error=str(e)) from e

    def get_query(self, search_query: dict) -> List[Dyntastic]:
        """Get result for a certain dynamodb search query.

        Args:
            search_query (str): serialized search query.

        Returns:
            T: The query related item, or None.

        Raises:
            ValidationException: If the query is invalid.
        """
        try:
            print("Search query :", search_query)
            response = self.model.query(**search_query)
            query_items = [item.__dict__ for item in response]
            return query_items
        except ValidationException as e:
            raise ValidationException("The search query format is invalid.") from e

    def delete_one(self, id: str) -> Dyntastic:
        """Delete an item from the DynamoDB table by its ID.

        Args:
            id (str): The unique identifier of the item to delete.

        Returns:
            Dyntastic: The deleted item.

        Raises:
            ItemNotFoundException: If the item does not exist.
            DataModelException: If an error occurs while deleting the item.
        """
        try:
            item = self.model.get(id)
            if item:
                item.delete()
                return item
            else:
                raise ItemNotFoundException(item_id=id)
        except DoesNotExist:
            raise ItemNotFoundException(item_id=id)
        except Exception as e:
            raise DataModelException(error=str(e)) from e

    def delete_all(self) -> List[Dyntastic]:
        """Delete all items in the DynamoDB table.

        Returns:
            List[T]: A list of all deleted items.

        Raises:
            DataModelException: If an error occurs while deleting items.
        """
        try:
            items = list(self.model.scan())
            for item in items:
                item.delete()
            return items
        except Exception as e:
            raise DataModelException(error=str(e)) from e
