# Standard Library
from typing import Dict

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.serve import (
    ProtocolV1RequestModel,
    ProtocolV1ResponseModel,
)


class KeywordsPredictRequestModel(ProtocolV1RequestModel):

    pass


class KeywordsPredictResponseModel(ProtocolV1ResponseModel):

    pass


class KeywordsBioResponseModel(BaseModel):

    name: str = "keywords-model"
    # difficult to link up all the way back to the `CompiledKeywordsTrackedModelCard` here, so for
    # now we leave this unmodelled ith an understanding that that is what will come through in this
    # field
    tracked_keywords_model_card: Dict
