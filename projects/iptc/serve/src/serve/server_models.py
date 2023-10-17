"""Prediction data schemas."""

# Standard Library
from typing import Dict, List, Optional

# 3rd party libraries
from pydantic import BaseModel


# --- prediction request models
class PredictConfiguration(BaseModel):
    """Configuration for prediction request.

    Attributes:
        language (Optional[str]): Language used for prediction. Defaults to "en"
    """

    language: Optional[str] = "en"


class PredictInputContentModel(BaseModel):
    """Input content for a prediction rerquest.

    Attributes:
        content (str): The input content for prediction
    """

    content: str


class PredictRequestModel(BaseModel):
    """Request model for making a prediction.

    Attributes:
        inputs (PredictInputContentModel): The input content for prediction
    """

    configuration: Optional[PredictConfiguration] = PredictConfiguration()
    inputs: PredictInputContentModel


class PredictionExtractedIPTC(BaseModel):
    """Extracted iptc information from a prediction.

    Attributes:
        label (str): The iptc label of the article.
        score (float): softmax score of iptc
    """

    label: str
    score: float


class PredictionOutputContent(BaseModel):
    """Output content containing extracted iptc from a prediction.

    Attributes:
        predicted_content (List[PredictionExtractedIPTC]): List of extracted iptc
    """

    predicted_content: List[PredictionExtractedIPTC]


class PredictResponseModel(BaseModel):
    """Response model for a prediction request.

    Attributes:
        output (PredictionOutputContent): The output content containing extracted iptc
    """

    outputs: PredictionOutputContent


# --- bio response models
class BioResponseModel(BaseModel):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "iptc-model"
    model_card: Dict
