"""General Purpose CRUD Router."""

# Standard Library
from typing import Any, Callable, Dict, List, Optional, Type, Union

# 3rd party libraries
from fastapi import HTTPException
from pydantic import BaseModel

# Internal libraries
from onclusiveml.data.data_model.base import BaseDataModel
from onclusiveml.data.data_model.exception import (
    DataModelException,
    ItemNotFoundException,
    ValidationException,
)
from onclusiveml.serving.rest.crud._base import CRUDGenerator
from onclusiveml.serving.rest.crud._types import depends


CALLABLE = Callable[..., BaseModel]
CALLABLE_LIST = Callable[..., List[BaseModel]]


class CRUDRouter(CRUDGenerator[BaseModel]):
    """A general-purpose CRUD router for FastAPI.

    This class extends the CRUDGenerator to provide CRUD endpoints
    for any data model that inherits from BaseDataModel.
    """

    def __init__(
        self,
        schema: Type[BaseModel],
        model: BaseDataModel[Any],
        create_schema: Optional[Type[BaseModel]] = None,
        update_schema: Optional[Type[BaseModel]] = None,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        paginate: Optional[int] = None,
        get_all_route: Union[bool, depends] = True,
        get_one_route: Union[bool, depends] = True,
        create_route: Union[bool, depends] = True,
        update_route: Union[bool, depends] = True,
        delete_one_route: Union[bool, depends] = True,
        delete_all_route: Union[bool, depends] = True,
        **kwargs: Any,
    ) -> None:
        """Initialize the CRUDRouter.

        Args:
            schema (Type[BaseModel]): The Pydantic schema for the model.
            model (BaseDataModel): An instance of a data model.
            create_schema (Optional[Type[BaseModel]]): Schema for create operations.
            update_schema (Optional[Type[BaseModel]]): Schema for update operations.
            prefix (Optional[str]): URL prefix for the routes.
            tags (Optional[List[str]]): Tags for the routes.
            paginate (Optional[int]): Number of items per page for pagination.
            get_all_route (Union[bool, depends]): Enable/disable get all route.
            get_one_route (Union[bool, depends]): Enable/disable get one route.
            create_route (Union[bool, depends]): Enable/disable create route.
            update_route (Union[bool, depends]): Enable/disable update route.
            delete_one_route (Union[bool, depends]): Enable/disable delete one route.
            delete_all_route (Union[bool, depends]): Enable/disable delete all route.
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

        self.model = model  # Instance of BaseDataModel

    def _get_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        """Generate a route for retrieving all items with pagination.

        Returns:
            CALLABLE_LIST: A function that handles the get all route.
        """

        def route(
            pagination: Dict[str, Optional[int]] = self.pagination
        ) -> List[BaseModel]:
            try:
                skip, limit = pagination.get("skip"), pagination.get("limit")
                skip = skip or 0  # Default to 0 if None

                items = self.model._get_all()
                items = items[skip:] if limit is None else items[skip : skip + limit]

                return [self.schema(**item.__dict__) for item in items]
            except DataModelException as e:
                # Handle known data model exceptions
                raise HTTPException(status_code=400, detail=str(e)) from e
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

        def route(item_id: str) -> BaseModel:
            try:
                item = self.model._get_one(item_id)
                return self.schema(**item.__dict__)
            except ItemNotFoundException as e:
                raise HTTPException(status_code=404, detail=str(e)) from e
            except DataModelException as e:
                raise HTTPException(status_code=400, detail=str(e)) from e
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

        def route(model_data: self.create_schema) -> BaseModel:
            try:
                item = self.model._create(model_data.dict())
                return self.schema(**item.__dict__)
            except ValidationException as ve:
                raise HTTPException(status_code=400, detail=str(ve)) from ve
            except DataModelException as e:
                raise HTTPException(status_code=400, detail=str(e)) from e
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

        def route(item_id: str, model_data: self.update_schema) -> BaseModel:
            try:
                update_data = model_data.dict(exclude_unset=True)
                item = self.model._update(item_id, update_data)
                return self.schema(**item.__dict__)
            except ItemNotFoundException as e:
                raise HTTPException(status_code=404, detail=str(e)) from e
            except ValidationException as ve:
                raise HTTPException(status_code=400, detail=str(ve)) from ve
            except DataModelException as e:
                raise HTTPException(status_code=400, detail=str(e)) from e
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

        def route() -> List[BaseModel]:
            try:
                items = self.model._delete_all()
                return [self.schema(**item.__dict__) for item in items]
            except DataModelException as e:
                raise HTTPException(status_code=400, detail=str(e)) from e
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

        def route(item_id: str) -> BaseModel:
            try:
                item = self.model._delete_one(item_id)
                return self.schema(**item.__dict__)
            except ItemNotFoundException as e:
                raise HTTPException(status_code=404, detail=str(e)) from e
            except DataModelException as e:
                raise HTTPException(status_code=400, detail=str(e)) from e
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Internal server error: {str(e)}"
                )

        return route
