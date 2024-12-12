"""DcumentDB Data Model."""

# Standard Library
from typing import Any, Dict, List

# 3rd party libraries
import mongomock
from dyntastic import Dyntastic
from dyntastic.exceptions import DoesNotExist
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository
from pydantic_settings import BaseSettings, SettingsConfigDict
from pymongo import MongoClient

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.data.data_model.base import BaseDataModel
from onclusiveml.data.data_model.exception import (
    DataModelException,
    ItemNotFoundException,
    ValidationException,
)


class ConnectionSettings(OnclusiveBaseSettings):
    """Tracked NER model specs."""

    username: str
    password: str
    endpoint: str
    port: int
    ca_file_path: str
    database_name: str
    collection_name: str

    model_config = SettingsConfigDict(env_prefix="documentdb_")


settings = ConnectionSettings()


class DocumentDBModel:
    """A data model class for interacting with DB tables.

    This class provides methods for CRUD operations on DB tables
    using the Dyntastic library for object mapping.
    """

    def __init__(self, model, database_name_input, collection_name_input, test=False):
        self.model = model
        self.test = test
        self.client = self.get_client()
        self.table = self.create_table(database_name_input, collection_name_input)

    def get_client(self) -> Any:
        if self.test:
            return mongomock.MongoClient()
        # Create the MongoDB client connection string
        connection_string = (
            f"mongodb://{settings.username}:{settings.password}@{settings.endpoint}:{settings.port}/"
            f"?tls=true&tlsCAFile={settings.ca_file_path}&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
        )
        # Connect to Amazon DocumentDB
        client = MongoClient(connection_string)
        return client

    def create_table(self, database_name_input, collection_name_input):
        class DocumentDBModelInner(AbstractRepository[self.model]):
            class Meta:
                collection_name = collection_name_input

        database = self.client[database_name_input]
        table = DocumentDBModelInner(database=database)
        return table

    @property
    def table_name(self) -> str:
        """Return the name of the DcumentDB table associated with the model.

        Returns:
            str: The name of the DcumentDB table.
        """
        return self.table._AbstractRepository__collection_name

    def get_all(self) -> List[Dyntastic]:
        """Fetch all items from the DcumentDB table.

        Returns:
            List[T]: A list of all items in the table.

        Raises:
            DataModelException: If an error occurs while fetching items.
        """
        try:
            return list(self.table.find_by({}))
        except Exception as e:
            raise DataModelException(error=str(e)) from e

    def get_one(self, id: str) -> Dyntastic:
        """Fetch a single item from the DcumentDB table by its ID.

        Args:
            id (str): The unique identifier of the item.

        Returns:
            Dyntastic: The item with the specified ID.

        Raises:
            ItemNotFoundException: If the item does not exist.
            DataModelException: If an error occurs while fetching the item.
        """
        try:
            item = self.table.find_one_by_id(id)
        except DoesNotExist:
            raise ItemNotFoundException(item_id=id)
        except Exception as e:
            raise DataModelException(error=str(e)) from e

        if item is None:
            raise ItemNotFoundException(item_id=id)

        return item

    def create(self, item: Dict[str, Any]) -> Dyntastic:
        """Create a new item in the DcumentDB table.

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
            self.table.save(new_item)
            return new_item
        except ValueError as ve:
            raise ValidationException(error=str(ve)) from ve
        except Exception as e:
            raise DataModelException(error=str(e)) from e

    def update(self, id: str, item: Dict[str, Any]) -> Dyntastic:
        """Update an existing item in the DcumentDB table.

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
            existing_item = self.table.find_one_by_id(id)
        except DoesNotExist:
            raise ItemNotFoundException(item_id=id)
        except ValueError as ve:
            raise ValidationException(error=str(ve)) from ve
        except Exception as e:
            raise DataModelException(error=str(e)) from e

        if not existing_item:
            raise ItemNotFoundException(item_id=id)

        for key, value in item.items():
            setattr(existing_item, key, value)
        self.table.save(existing_item)

        return existing_item

    def get_query(self, search_query: dict) -> List[Dyntastic]:
        """Get result for a certain Dcumentdb search query.

        Args:
            search_query (str): serialized search query.

        Returns:
            T: The query related item, or None.

        Raises:
            ValidationException: If the query is invalid.
        """
        try:
            response = self.table.find_by(search_query)
            query_items = [item for item in response]
            return query_items
        except ValidationException as e:
            raise ValidationException("The search query format is invalid.") from e

    def delete_one(self, id: str) -> Dyntastic:
        """Delete an item from the DcumentDB table by its ID.

        Args:
            id (str): The unique identifier of the item to delete.

        Returns:
            Dyntastic: The deleted item.

        Raises:
            ItemNotFoundException: If the item does not exist.
            DataModelException: If an error occurs while deleting the item.
        """
        try:
            item = self.table.find_one_by_id(id)
            if item:
                self.table.delete(item)
                return item
        except DoesNotExist:
            raise ItemNotFoundException(item_id=id)
        except Exception as e:
            raise DataModelException(error=str(e)) from e

        if not item:
            raise ItemNotFoundException(item_id=id)

    def delete_all(self) -> List[Dyntastic]:
        """Delete all items in the DcumentDB table.

        Returns:
            List[T]: A list of all deleted items.

        Raises:
            DataModelException: If an error occurs while deleting items.
        """
        try:
            items = list(self.table.find_by({}))
            for item in items:
                self.table.delete(item)
            return items
        except Exception as e:
            raise DataModelException(error=str(e)) from e
