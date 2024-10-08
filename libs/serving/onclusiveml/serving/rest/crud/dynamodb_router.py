"""DynamoDB CRUD Router."""

# Standard Library
from typing import Any, Callable, List, Optional, Type, Union

# 3rd party libraries
from fastapi import HTTPException
from fastapi_crudrouter.core._base import CRUDGenerator
from fastapi_crudrouter.core._types import DEPENDENCIES, PAGINATION
from fastapi_crudrouter.core._types import PYDANTIC_SCHEMA as SCHEMA

# Internal libraries
from onclusiveml.data.data_model.dynamodb_model.dynamodb_model import (
    DynamoDBModel,
)


CALLABLE = Callable[..., SCHEMA]
CALLABLE_LIST = Callable[..., List[SCHEMA]]


class DynamoDBCRUDRouter(CRUDGenerator[SCHEMA]):
    """A CRUD router for DynamoDB operations using FastAPI.

    This class extends the CRUDGenerator to provide CRUD operations
    specifically for DynamoDB tables using the DynamoDBModel.
    """

    def __init__(
        self,
        schema: Type[SCHEMA],
        model: DynamoDBModel,
        create_schema: Optional[Type[SCHEMA]] = None,
        update_schema: Optional[Type[SCHEMA]] = None,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        paginate: Optional[int] = None,
        get_all_route: Union[bool, DEPENDENCIES] = True,
        get_one_route: Union[bool, DEPENDENCIES] = True,
        create_route: Union[bool, DEPENDENCIES] = True,
        update_route: Union[bool, DEPENDENCIES] = True,
        delete_one_route: Union[bool, DEPENDENCIES] = True,
        delete_all_route: Union[bool, DEPENDENCIES] = True,
        **kwargs: Any,
    ) -> None:
        """Initialize the DynamoDBCRUDRouter.

        Args:
            schema (Type[SCHEMA]): The Pydantic schema for the model.
            model (DynamoDBModel): An instance of DynamoDBModel.
            create_schema (Optional[Type[SCHEMA]]): Schema for create operations.
            update_schema (Optional[Type[SCHEMA]]): Schema for update operations.
            prefix (Optional[str]): URL prefix for the routes.
            tags (Optional[List[str]]): Tags for the routes.
            paginate (Optional[int]): Number of items per page for pagination.
            get_all_route (Union[bool, DEPENDENCIES]): Enable/disable get all route.
            get_one_route (Union[bool, DEPENDENCIES]): Enable/disable get one route.
            create_route (Union[bool, DEPENDENCIES]): Enable/disable create route.
            update_route (Union[bool, DEPENDENCIES]): Enable/disable update route.
            delete_one_route (Union[bool, DEPENDENCIES]): Enable/disable delete one route.
            delete_all_route (Union[bool, DEPENDENCIES]): Enable/disable delete all route.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            schema=schema,
            create_schema=create_schema,
            update_schema=update_schema,
            prefix=prefix,
            tags=tags,
            paginate=paginate,
            get_all_route=get_all_route,
            get_one_route=get_one_route,
            create_route=create_route,
            update_route=update_route,
            delete_one_route=delete_one_route,
            delete_all_route=delete_all_route,
            **kwargs,
        )

        self.model = model  # Instance of DynamoDBModel

    def _get_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        """Generate a route for retrieving all items with pagination.

        Returns:
            CALLABLE_LIST: A function that handles the get all route.
        """

        def route(pagination: PAGINATION = self.pagination) -> List[SCHEMA]:
            try:
                skip, limit = pagination.get("skip"), pagination.get("limit")
                skip = skip or 0  # Default to 0 if None

                items = self.model._get_all()
                items = items[skip:] if limit is None else items[skip : skip + limit]

                return [self.schema(**item.__dict__) for item in items]
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Internal server error: {str(e)}"
                )

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        """Generate a route for retrieving a single item by ID.

        Returns:
            CALLABLE: A function that handles the get one route.
        """

        def route(item_id: str) -> SCHEMA:
            try:
                item = self.model._get_one(item_id)
                if item is None:
                    raise HTTPException(
                        status_code=404, detail=f"Item with id {item_id} not found"
                    )
                return self.schema(**item.__dict__)
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Internal server error: {str(e)}"
                )

        return route

    def _create(self, *args: Any, **kwargs: Any) -> CALLABLE:
        """Generate a route for creating a new item.

        Returns:
            CALLABLE: A function that handles the create route.
        """

        def route(model_data: self.create_schema) -> SCHEMA:
            try:
                item = self.model._create(model_data.dict())
                return self.schema(**item.__dict__)
            except ValueError as ve:
                raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Internal server error: {str(e)}"
                )

        return route

    def _update(self, *args: Any, **kwargs: Any) -> CALLABLE:
        """Generate a route for updating an existing item.

        Returns:
            CALLABLE: A function that handles the update route.
        """

        def route(item_id: str, model_data: self.update_schema) -> SCHEMA:
            try:
                item = self.model._update(item_id, model_data.dict())
                if item is None:
                    raise HTTPException(
                        status_code=404, detail=f"Item with id {item_id} not found"
                    )
                return self.schema(**item.__dict__)
            except HTTPException:
                raise
            except ValueError as ve:
                raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Internal server error: {str(e)}"
                )

        return route

    def _delete_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        """Generate a route for deleting all items.

        Returns:
            CALLABLE_LIST: A function that handles the delete all route.
        """

        def route() -> List[SCHEMA]:
            try:
                items = self.model._delete_all()
                return [self.schema(**item.__dict__) for item in items]
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Internal server error: {str(e)}"
                )

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        """Generate a route for deleting a single item by ID.

        Returns:
            CALLABLE: A function that handles the delete one route.
        """

        def route(item_id: str) -> SCHEMA:
            try:
                item = self.model._delete_one(item_id)
                if item is None:
                    raise HTTPException(
                        status_code=404, detail=f"Item with id {item_id} not found"
                    )
                return self.schema(**item.__dict__)
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Internal server error: {str(e)}"
                )

        return route
