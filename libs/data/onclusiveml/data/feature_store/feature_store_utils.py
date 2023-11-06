"""Utilities for feast feature store."""

# 3rd party libraries
from pydantic import BaseSettings


class FeatureStoreParams(BaseSettings):
    """Base class for all parameter classes in the featurestore module in data library.

    Subclassing from BaseSettings allows for configuring parameters via environment variables.
    """

    pass
