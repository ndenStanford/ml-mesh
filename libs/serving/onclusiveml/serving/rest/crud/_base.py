"""Base CRUD Generator."""

# Standard Library
from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, List, Optional, Type, TypeVar, Union

# 3rd party libraries
from fastapi import APIRouter, HTTPException
from fastapi.types import DecoratedCallable
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.crud._types import depends
from onclusiveml.serving.rest.crud._utils import (
    pagination_factory,
    schema_factory,
)


T = TypeVar("T", bound=BaseModel)
NOT_FOUND = HTTPException(404, "Item not found")


class CRUDGenerator(Generic[T], APIRouter, ABC):
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
        create_schema: Optional[Type[T]] = None,
        update_schema: Optional[Type[T]] = None,
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
        """Initialize the CRUDGenerator.

        Args:
            schema (Type[T]): The Pydantic model to generate CRUD routes for.
            create_schema (Optional[Type[T]], optional): The schema used for create operations
            update_schema (Optional[Type[T]], optional): The schema used for update operations
            prefix (Optional[str], optional): The URL prefix for the routes
            tags (Optional[List[str]], optional): The list of tags for the routes.
            paginate (Optional[int], optional): The maximum number of items per page for pagination
            get_all_route (Union[bool, depends], optional): Whether to include the get_all route
            get_one_route (Union[bool, depends], optional): Whether to include the get_one route
            create_route (Union[bool, depends], optional): Whether to include the create route
            update_route (Union[bool, depends], optional): Whether to include the update route
            delete_one_route (Union[bool, depends], optional): Whether to include the delete_one
            delete_all_route (Union[bool, depends], optional): Whether to include the delete_all
            **kwargs: Additional keyword arguments passed to the APIRouter.
        """
        self.schema = schema
        self.pagination = pagination_factory(max_limit=paginate)
        self._pk: str = self._pk if hasattr(self, "_pk") else "id"
        self.create_schema = (
            create_schema
            if create_schema
            else schema_factory(self.schema, pk_field_name=self._pk, name="Create")
        )
        self.update_schema = (
            update_schema
            if update_schema
            else schema_factory(self.schema, pk_field_name=self._pk, name="Update")
        )

        prefix = str(prefix if prefix else self.schema.__name__).lower()
        prefix = self._base_path + prefix.strip("/")
        tags = tags or [prefix.strip("/").capitalize()]

        super().__init__(prefix=prefix, tags=tags, **kwargs)

        if get_all_route:
            self._add_api_route(
                "",
                self._get_all(),
                methods=["GET"],
                response_model=Optional[List[self.schema]],  # type: ignore
                summary="Get All",
                dependencies=get_all_route,
            )

        if create_route:
            self._add_api_route(
                "",
                self._create(),
                methods=["POST"],
                response_model=self.schema,
                summary="Create One",
                dependencies=create_route,
            )

        if delete_all_route:
            self._add_api_route(
                "",
                self._delete_all(),
                methods=["DELETE"],
                response_model=Optional[List[self.schema]],  # type: ignore
                summary="Delete All",
                dependencies=delete_all_route,
            )

        if get_one_route:
            self._add_api_route(
                "/{item_id}",
                self._get_one(),
                methods=["GET"],
                response_model=self.schema,
                summary="Get One",
                dependencies=get_one_route,
                error_responses=[NOT_FOUND],
            )

        if update_route:
            self._add_api_route(
                "/{item_id}",
                self._update(),
                methods=["PUT"],
                response_model=self.schema,
                summary="Update One",
                dependencies=update_route,
                error_responses=[NOT_FOUND],
            )

        if delete_one_route:
            self._add_api_route(
                "/{item_id}",
                self._delete_one(),
                methods=["DELETE"],
                response_model=self.schema,
                summary="Delete One",
                dependencies=delete_one_route,
                error_responses=[NOT_FOUND],
            )

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

    def get(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """Add or override a GET route.

        Args:
            path (str): The URL path for the route.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Callable[[DecoratedCallable], DecoratedCallable]: A decorator function.
        """
        self.remove_api_route(path, ["GET"])
        return super().get(path, *args, **kwargs)

    def post(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """Add or override a POST route.

        Args:
            path (str): The URL path for the route.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Callable[[DecoratedCallable], DecoratedCallable]: A decorator function.
        """
        self.remove_api_route(path, ["POST"])
        return super().post(path, *args, **kwargs)

    def put(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """Add or override a PUT route.

        Args:
            path (str): The URL path for the route.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Callable[[DecoratedCallable], DecoratedCallable]: A decorator function.
        """
        self.remove_api_route(path, ["PUT"])
        return super().put(path, *args, **kwargs)

    def delete(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """Add or override a DELETE route.

        Args:
            path (str): The URL path for the route.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Callable[[DecoratedCallable], DecoratedCallable]: A decorator function.
        """
        self.remove_api_route(path, ["DELETE"])
        return super().delete(path, *args, **kwargs)

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

    @abstractmethod
    def _get_all(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """Abstract method for getting all items.

        Must be implemented in subclasses.

        Raises:
            NotImplementedError: If not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_one(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """Abstract method for getting a single item by ID.

        Must be implemented in subclasses.

        Raises:
            NotImplementedError: If not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def _create(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """Abstract method for creating a new item.

        Must be implemented in subclasses.

        Raises:
            NotImplementedError: If not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def _update(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """Abstract method for updating an existing item.

        Must be implemented in subclasses.

        Raises:
            NotImplementedError: If not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def _delete_one(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """Abstract method for deleting a single item by ID.

        Must be implemented in subclasses.

        Raises:
            NotImplementedError: If not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def _delete_all(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """Abstract method for deleting all items.

        Must be implemented in subclasses.

        Raises:
            NotImplementedError: If not implemented.
        """
        raise NotImplementedError

    def _raise(self, e: Exception, status_code: int = 422) -> HTTPException:
        """Raise an HTTPException with the given status code.

        Args:
            e (Exception): The exception to raise.
            status_code (int, optional): The HTTP status code.

        Raises:
            HTTPException: The HTTP exception with the specified status code and error message.
        """
        raise HTTPException(status_code, ", ".join(e.args)) from e

    @staticmethod
    def get_routes() -> List[str]:
        """Get the list of CRUD routes.

        Returns:
            List[str]: A list of route names.
        """
        return ["get_all", "create", "delete_all", "get_one", "update", "delete_one"]
