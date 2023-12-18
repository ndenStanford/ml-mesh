"""Custom HTTP exceptions."""

# 3rd party libraries
from fastapi import HTTPException


class OnclusiveHTTPException(HTTPException):
    """Onclusive base class for HTTP exceptions."""
