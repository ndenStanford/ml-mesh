"""IPTC v1 data schemas."""

# Standard Library
from typing import List, Optional

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data.

    Attributes:
        content (str):
    """

    content: str = ""


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""


class PredictResponseIPTC(JsonApiSchema):
    """Prediction iptc."""

    label: Optional[str] = None
    score: Optional[float] = None
    mediatopic_id: Optional[str] = None


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data.

    Attributes:
        iptc (label): list of iptc of the article
    """

    iptc_topic: List[PredictResponseIPTC] = []


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
    """

    model_name: str = "iptc-multi"
