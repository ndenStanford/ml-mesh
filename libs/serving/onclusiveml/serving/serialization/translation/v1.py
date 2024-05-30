"""Entity linking v1 data schemas."""

# Standard Library
from typing import Optional

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    content: str
    target_lang: str


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""

    lang: Optional[str] = None
    brievety: bool = False
    lang_detect: bool = False
    translation: bool = False


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    original_language: Optional[str] = None
    target_language: Optional[str] = None
    translation: Optional[str] = None


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (Dict): Information about the model
    """

    model_name: str
