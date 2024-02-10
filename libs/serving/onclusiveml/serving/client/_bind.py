"""Bind method."""

# Standard Library
import os
from typing import Any, Callable, Dict, List, Tuple
from urllib.parse import urljoin

# 3rd party libraries
import requests
from pydantic.tools import parse_obj_as

# Internal libraries
from onclusiveml.core.serialization import (
    JsonApiSchema,
    JsonApiSchemas,
    RequestSchema,
    ResponseSchema,
)
from onclusiveml.serving.client.exceptions import (
    OnclusiveMachineLearningAPIError,
)


def bind(**kwargs: Dict[str, Any]) -> Callable:
    """Binds model API call method to client class.

    Args:
        client (Any): Onclusive API Client instance.
        namespace (str): API namespace (i.e. project name).
        versions (int): model versions supported.
        request_parameters_schema (List[JsonApiSchema]):
        request_attributes_schema (List[JsonApiSchema]):
        response_attributes_schema (List[JsonApiSchema]):
    """

    class OnclusiveApiMethod:
        """Api Method.

        Attributes:
            client (Any):
            namespace (str):
            endpoint (str):
            version (int):
            method (str):
            request_parameters_schema (JsonApiSchema):
            input_schemas (JsonApiSchema):
            output_schema (JsonApiSchema):
        """

        namespace: str = str(kwargs["namespace"])
        endpoint: str = str(kwargs["endpoint"])
        method: str = str(kwargs["method"])
        version: str = str(kwargs["version"])
        request_parameters_schema: JsonApiSchema = kwargs["request_parameters_schema"]
        request_attributes_schema: JsonApiSchema = kwargs["request_attributes_schema"]
        response_attributes_schema: JsonApiSchema = kwargs["response_attributes_schema"]

        def __init__(self, client: Any, *args: List, **kwargs: Dict) -> None:
            self.client = client
            self.args = args
            self.request_kwargs = kwargs

        @property
        def url(self) -> str:
            return os.path.join(self.path, f"v{self.version}", self.endpoint)

        @property
        def headers(self) -> Dict[str, str]:
            """API call headers."""
            return {
                self.client.api_key_header: self.client.api_key,
                "content-type": "application/json",
            }

        @property
        def request(self) -> RequestSchema:
            """Get request."""
            attributes = {
                field: self.request_kwargs[field]
                for field in self.request_attributes_schema.__fields__.keys()
            }
            parameters = {
                field: self.request_kwargs[field]
                for field in self.request_parameters_schema.__fields__.keys()
            }
            # generate API models based on input schemas.
            Request, _ = self.schemas

            return Request.from_data(
                namespace=self.namespace, attributes=attributes, parameters=parameters
            )

        @property
        def path(self) -> str:
            """API call full path."""
            return urljoin(
                f"{self.client.protocol}://{self.client.host}", self.namespace
            )

        @property
        def schemas(self) -> Tuple[RequestSchema, ResponseSchema]:
            """Request and Response schemas."""
            return JsonApiSchemas(
                namespace=self.namespace,
                request_attributes_schema=self.request_attributes_schema,
                response_attributes_schema=self.response_attributes_schema,
                request_parameters_schema=self.request_parameters_schema,
            )

        def execute(self) -> ResponseSchema:
            """Execute API query."""
            print("+" * 30)
            print(self.method)
            print(self.url)
            print(self.headers)
            print(self.request.dict())
            response = requests.request(
                self.method, self.url, headers=self.headers, json=self.request.dict()
            )
            _, Response = self.schemas
            if response.status_code >= 300:
                raise OnclusiveMachineLearningAPIError(code=response.status_code)
            return parse_obj_as(Response, response.json())

    def _call(client: Any, **kwargs: Dict) -> Callable:
        """Wrapper around api method execution."""
        return OnclusiveApiMethod(client=client, **kwargs).execute()

    return _call
