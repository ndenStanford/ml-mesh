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

    lang: str = "en"
    brievety: bool = False


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    translation: Optional[str] = None


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (Dict): Information about the model
    """

    model_name: str
