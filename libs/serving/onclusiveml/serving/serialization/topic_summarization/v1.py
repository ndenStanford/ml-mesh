"""Topic Summarization v1 data schemas."""

# Standard Library
from typing import Dict, List, Optional, Union

# Internal libraries
from onclusiveml.core.base.utils import OnclusiveEnum
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    content: Optional[List[str]] = None
    topic_id: Optional[int] = None
    query_string: Optional[str] = None
    trend_detection: Optional[bool] = True
    query_id: Optional[str] = None
    media_api_version: Optional[str] = "1"
    save_report_dynamodb: bool = False


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""


class ImpactCategoryLabel(str, OnclusiveEnum):
    """Impact category label."""

    LOW = "low"
    MID = "mid"
    HIGH = "high"


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    topic: Optional[Dict[str, Optional[Union[str, Dict[str, str]]]]]
    impact_category: Optional[ImpactCategoryLabel]


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "topic-summarization"
