"""Pydantic based base classes."""

# Standard Library
from typing import Type

# 3rd party libraries
from pydantic import BaseModel, PlainSerializer, SecretStr
from pydantic_settings import BaseSettings
from typing_extensions import Annotated

# Internal libraries
from onclusiveml.core.base.exception import BaseClassNotFound


OnclusiveSecretStr = Annotated[
    SecretStr, PlainSerializer(lambda x: x.get_secret_value(), return_type=str)
]


class OnclusiveBaseSettings(BaseSettings):
    """Base class for all parameter classes in the core library."""

    class Config:
        extra = "forbid"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class OnclusiveFrozenSettings(OnclusiveBaseSettings):
    """Immutable Settings.

    After initialization, updating the attribute values
    will not be possible.
    """

    class Config:
        # make the service type immutable and hashable
        frozen = True
        validate_default = True


class OnclusiveBaseModel(BaseModel):
    """Base for all data models."""

    class Config:
        # Validate attributes when assigning them. We need to set this in order
        # to have a mix of mutable and immutable attributes
        validate_assignment = True
        #
        extra = "forbid"
        from_attributes = True


class OnclusiveFrozenModel(OnclusiveBaseModel):
    """Immutable data model."""

    class Config:
        # make the frozen schema immutable and hashable
        frozen = True
        arbitrary_types_allowed = True


def cast(
    obj: OnclusiveBaseSettings, t: Type[OnclusiveBaseSettings]
) -> OnclusiveBaseSettings:
    """Cast pydantic settings to parent class.

    Args:
        obj (OnclusiveBaseSettings): object to cast
        t: parent class
    """
    if t not in type(obj).__bases__:
        raise BaseClassNotFound(base=str(t), derived=type(obj))

    data = {k: getattr(obj, k) for k in t.schema().get("properties").keys()}

    return t(**data)
