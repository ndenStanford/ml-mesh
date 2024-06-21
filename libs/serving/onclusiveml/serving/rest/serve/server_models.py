"""Serving data models."""

# Standard Library
from typing import Any, Dict, List, Optional

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel, root_field_validator


class ServedModelMethods(OnclusiveBaseModel):
    """Served model methods.

    Utility to track the methods that a ServedModel subclass must implement
    to integrate with the `create_model_enpoint` utility method (see below).
    """

    predict: str = "predict"
    bio: str = "bio"


class ModelServerURLs(OnclusiveBaseModel):
    """Model server URLs."""

    root: str
    liveness: Optional[str] = ""
    readiness: Optional[str] = ""
    model_predict: Optional[str] = ""
    model_bio: Optional[str] = ""
    docs: Optional[str] = ""
    redoc: Optional[str] = ""
    openapi: Optional[str] = ""

    @root_field_validator
    def check_non_root_urls(cls, values: Dict) -> Dict:
        """Checks that each url indeed starts with the root url."""
        root_url = values["root"]

        assert root_url.startswith("/")

        for url_type in values.keys():
            if not values[url_type].startswith(root_url):
                raise ValueError(
                    f"Invalid non-root url for {url_type}: {values[url_type]} "
                    f"does not start with root url {root_url}"
                )

            if " " in values[url_type]:
                raise ValueError(
                    f"Invalid url for {url_type}: {values[url_type]} "
                    f"contains space(s)."
                )

        return values


class ReadinessProbeResponse(OnclusiveBaseModel):
    """Readiness probe."""

    ready: bool = True


class LivenessProbeResponse(OnclusiveBaseModel):
    """Liveness probe."""

    live: bool = True


class ProtocolV1RequestModel(OnclusiveBaseModel):
    """Request model."""

    instances: List[Any]


class ProtocolV1ResponseModel(OnclusiveBaseModel):
    """Response model."""

    predictions: List[Any]


class ServedModelBioModel(OnclusiveBaseModel):
    """Served model bio schema."""

    name: str
