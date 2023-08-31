"""Pydantic based base classes."""

# 3rd party libraries
from pydantic import BaseModel, BaseSettings


class OnclusiveBaseSettings(BaseSettings):
    """Base class for all parameter classes in the core library."""

    class Config:
        extra = "forbid"
        strict = True
        arbitrary_types_allowed = False
        validate_default = True
        # Validate attributes when assigning them. We need to set this in order
        # to have a mix of mutable and immutable attributes
        validate_assignment = True


class OnclusiveFrozenSettings(OnclusiveBaseSettings):
    """Immutable Settings.
    After initialization, updating the attribute values
    will not be possible.
    """

    class Config:
        allow_mutation = False
        # make the service type immutable and hashable
        frozen = True


class OnclusiveBaseSchema(BaseModel):
    """Base for all data models."""

    class Config:
        # Validate attributes when assigning them. We need to set this in order
        # to have a mix of mutable and immutable attributes
        validate_assignment = True
        #
        extra = "forbid"
        # all attributes with leading underscore are private and therefore
        # are mutable and not included in serialization
        underscore_attrs_are_private = True


class OnclusiveFrozenSchema(OnclusiveBaseSchema):
    """Immutable data model."""

    class Config:
        # make the frozen schema immutable and hashable
        allow_mutation = False
        frozen = True
