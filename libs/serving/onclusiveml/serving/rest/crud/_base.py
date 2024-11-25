"""Base CRUD Generator."""

# Standard Library
import ast
from typing import Any, Callable, Generic, List, Optional, Type, TypeVar, Union

# 3rd party libraries
from boto3.dynamodb.conditions import Key
from dyntastic import A
from fastapi import APIRouter, HTTPException, Query
from fastapi.types import DecoratedCallable

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel, OnclusiveFrozenSettings
from onclusiveml.data.data_model.base import BaseDataModel
from onclusiveml.data.data_model.exception import (
    DataModelException,
    ItemNotFoundException,
    ValidationException,
)
from onclusiveml.serving.rest.crud._types import depends


T = TypeVar("T", bound=OnclusiveBaseModel)


class CRUDGenerator(Generic[T], APIRouter):
    """Base class for generating CRUD routes in FastAPI.

    Taken from https://github.com/awtkns/fastapi-crudrouter/blob/2c18c90abf04b145f097da22044fa71e3ab3d52b/fastapi_crudrouter/core/_base.py.

    Provides methods to automatically generate CRUD endpoints for a given Pydantic schema.
    """  # noqa: W505

    schema: Type[T]
    create_schema: Type[T]
    update_schema: Type[T]
    _base_path: str = "/"

    def __init__(
        self,
        schema: Type[T],
        model: Type[BaseDataModel],
        create_schema: Optional[Type[T]] = None,
        update_schema: Optional[Type[T]] = None,
        api_settings: OnclusiveFrozenSettings = None,
        entity_name: str = "",
        tags: Optional[List[str]] = None,
        get_all_route: Union[bool, depends] = True,
        get_one_route: Union[bool, depends] = True,
        create_route: Union[bool, depends] = True,
        update_route: Union[bool, depends] = True,
        delete_one_route: Union[bool, depends] = True,
        delete_all_route: Union[bool, depends] = True,
        get_query_route: Union[bool, depends] = True,
        **kwargs: Any,
    ) -> None:
        """Initialize the CRUDGenerator.

        Args:
            schema (Type[T]): The Pydantic model to generate CRUD routes for.
            model (Type[BaseDataModel]): Child of base data model used to interact with database.
            create_schema (Optional[Type[T]], optional): The schema used for create operations
            update_schema (Optional[Type[T]], optional): The schema used for update operations
            api_settings: OnclusiveFrozenSettings: Service settings used to make route prefix
            entity_name: str: string used at the end of route prefix
            tags (Optional[List[str]], optional): The list of tags for the routes.
            get_all_route (Union[bool, depends], optional): Whether to include the get_all route
            get_one_route (Union[bool, depends], optional): Whether to include the get_one route
            create_route (Union[bool, depends], optional): Whether to include the create route
            update_route (Union[bool, depends], optional): Whether to include the update route
            delete_one_route (Union[bool, depends], optional): Whether to include the delete_one
            delete_all_route (Union[bool, depends], optional): Whether to include the delete_all
            get_query_route (Union[bool, depends], optional): Whether to include the get_query route
            **kwargs: Additional keyword arguments passed to the APIRouter.
        """
        self.schema = schema
        self.model = model
        self.create_schema = create_schema or schema
        self.update_schema = update_schema or schema

        prefix = f"/{api_settings.model_name}/{api_settings.api_version}/{entity_name}"
        prefix = self._base_path + prefix.strip("/")
        tags = tags or [prefix.strip("/").capitalize()]

        super().__init__(prefix=prefix, tags=tags, **kwargs)

        if get_query_route:
            self.add_api_route(
                "/query",
                self.get_route_get_query(),
                methods=["GET"],
                response_model=List[self.schema],
                summary="Get query",
                dependencies=(
                    get_query_route if isinstance(get_query_route, list) else []
                ),
            )

        if get_all_route:
            self.add_api_route(
                "",
                self.get_route_get_all(),
                methods=["GET"],
                response_model=List[self.schema],
                summary="Get All",
                dependencies=get_all_route if isinstance(get_all_route, list) else [],
            )

        if create_route:
            self.add_api_route(
                "",
                self.get_route_create(),
                methods=["POST"],
                response_model=self.schema,
                summary="Create One",
                dependencies=create_route if isinstance(create_route, list) else [],
            )

        if delete_all_route:
            self.add_api_route(
                "",
                self.get_route_delete_all(),
                methods=["DELETE"],
                response_model=List[self.schema],
                summary="Delete All",
                dependencies=(
                    delete_all_route if isinstance(delete_all_route, list) else []
                ),
            )

        if get_one_route:
            self.add_api_route(
                "/{item_id}",
                self.get_route_get_one(),
                methods=["GET"],
                response_model=self.schema,
                summary="Get One",
                dependencies=get_one_route if isinstance(get_one_route, list) else [],
            )

        if update_route:
            self.add_api_route(
                "/{item_id}",
                self.get_route_update(),
                methods=["PUT"],
                response_model=self.schema,
                summary="Update One",
                dependencies=update_route if isinstance(update_route, list) else [],
            )

        if delete_one_route:
            self.add_api_route(
                "/{item_id}",
                self.get_route_delete_one(),
                methods=["DELETE"],
                response_model=self.schema,
                summary="Delete One",
                dependencies=(
                    delete_one_route if isinstance(delete_one_route, list) else []
                ),
            )

    def get_route_get_all(self) -> Callable[..., Any]:
        """Create the route_get_all function."""

        def route_get_all():
            try:
                return self.model.get_all()
            except DataModelException as e:
                raise HTTPException(status_code=500, detail=str(e))

        return route_get_all

    def get_route_create(self) -> Callable[..., Any]:
        """Create the route_create function."""

        def route_create(item: self.create_schema):
            try:
                return self.model.create(item.dict())
            except ValidationException as e:
                raise HTTPException(status_code=422, detail=str(e))
            except DataModelException as e:
                raise HTTPException(status_code=500, detail=str(e))

        return route_create

    def get_route_delete_all(self) -> Callable[..., Any]:
        """Create the route_delete_all function."""

        def route_delete_all():
            try:
                return self.model.delete_all()
            except DataModelException as e:
                raise HTTPException(status_code=500, detail=str(e))

        return route_delete_all

    def get_route_get_one(self) -> Callable[..., Any]:
        """Create the route_get_one function."""

        def route_get_one(item_id: str):
            try:
                return self.model.get_one(item_id)
            except ItemNotFoundException:
                raise HTTPException(404, f"Item with id {item_id} does not exist.")
            except DataModelException as e:
                raise HTTPException(status_code=500, detail=str(e))

        return route_get_one

    def get_route_update(self) -> Callable[..., Any]:
        """Create the route_update function."""

        def route_update(item_id: str, item: self.update_schema):
            try:
                return self.model.update(item_id, item.dict(exclude_unset=True))
            except ItemNotFoundException:
                raise HTTPException(404, f"Item with id {item_id} does not exist.")
            except ValidationException as e:
                raise HTTPException(status_code=422, detail=str(e))
            except DataModelException as e:
                raise HTTPException(status_code=500, detail=str(e))

        return route_update

    def get_route_delete_one(self) -> Callable[..., Any]:
        """Create the route_delete_one function."""

        def route_delete_one(item_id: str):
            try:
                return self.model.delete_one(item_id)
            except ItemNotFoundException:
                raise HTTPException(404, f"Item with id {item_id} does not exist.")
            except DataModelException as e:
                raise HTTPException(status_code=500, detail=str(e))

        return route_delete_one

    def get_route_get_query(self) -> Callable[..., Any]:
        """Create the route_get_query function."""

        def parse_condition(condition_str: str):
            """Parses a condition string and combines conditions with logical AND (&)."""
            if " & " in condition_str:
                # Split by the & operator and evaluate each part
                parts = condition_str.split(" & ")
                parsed_conditions = [
                    eval(part, {}, {"A": A, "Key": Key}) for part in parts
                ]
                # Combine all parts with &
                combined_condition = parsed_conditions[0]
                for condition in parsed_conditions[1:]:
                    combined_condition &= condition
                return combined_condition
            else:
                # Single condition
                return eval(condition_str, {}, {"A": A, "Key": Key})

        def route_get_query(serialized_query: str = Query(...)):
            try:
                json_query = ast.literal_eval(serialized_query)
                search_query = {
                    k: (
                        parse_condition(v)
                        if (v.startswith("Key(") or v.startswith("A("))
                        else v
                    )
                    for k, v in json_query.items()
                }
                return self.model.get_query(search_query)
            except ValidationException:
                raise HTTPException(404, f"Query {serialized_query} is not valid.")

        return route_get_query

    def _add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        dependencies: Union[bool, depends],
        error_responses: Optional[List[HTTPException]] = None,
        **kwargs: Any,
    ) -> None:
        """Add an API route to the router.

        Args:
            path (str): The URL path for the route.
            endpoint (Callable[..., Any]): The endpoint function.
            dependencies (Union[bool, depends]): Dependencies or a boolean indicating whether to include dependencies.
            error_responses (Optional[List[HTTPException]], optional): List of HTTP exceptions
            **kwargs: Additional keyword arguments passed to add_api_route.
        """
        dependencies = [] if isinstance(dependencies, bool) else dependencies
        responses: Any = (
            {err.status_code: {"detail": err.detail} for err in error_responses}
            if error_responses
            else None
        )

        super().add_api_route(
            path, endpoint, dependencies=dependencies, responses=responses, **kwargs
        )

    def api_route(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """Add or override an API route.

        Overrides an existing route if it exists.

        Args:
            path (str): The URL path for the route.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Callable[[DecoratedCallable], DecoratedCallable]: A decorator function.
        """
        methods = kwargs["methods"] if "methods" in kwargs else ["GET"]
        self.remove_api_route(path, methods)
        return super().api_route(path, *args, **kwargs)

    def remove_api_route(self, path: str, methods: List[str]) -> None:
        """Remove an API route from the router.

        Args:
            path (str): The URL path of the route to remove.
            methods (List[str]): The HTTP methods of the route to remove.
        """
        methods_ = set(methods)

        for route in self.routes:
            if (
                route.path == f"{self.prefix}{path}"  # type: ignore
                and route.methods == methods_  # type: ignore
            ):
                self.routes.remove(route)

    @staticmethod
    def get_routes() -> List[str]:
        """Get the list of CRUD routes.

        Returns:
            List[str]: A list of route names.
        """
        return [
            "get_all",
            "create",
            "delete_all",
            "get_one",
            "update",
            "delete_one",
            "get_query",
        ]
