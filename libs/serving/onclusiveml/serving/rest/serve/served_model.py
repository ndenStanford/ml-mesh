# Standard Library
from typing import Dict, Union

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.serve.server_models import (
    ProtocolV1RequestModel,
    ProtocolV1ResponseModel,
)
from onclusiveml.tracking import TrackedModelCard


class ServedModel(object):
    """A wrapper class for bringing in any machine learning model into the ModelServer serving
    utility class for serving ML predictions via REST.

    Roughly follows the kserve.Model implementation."""

    name: str = "served_model"
    predict_request_model: BaseModel = ProtocolV1RequestModel
    predict_response_model: BaseModel = ProtocolV1ResponseModel
    bio_response_model: BaseModel = TrackedModelCard

    def __init__(self, name: str, api_version: str = "v1") -> None:

        self.name = name
        self.api_version = api_version
        self.ready = False

    def load(self) -> None:
        """Loading the model artifacts and readying the model for inference. After calling this
        method, the model needs to be ready for inference.
        """

        self.ready = True

    def is_ready(self) -> bool:
        """Customizable readyness probe backend that considers the state of the served model"""

        return self.ready

    def predict(
        self, payload: predict_request_model
    ) -> Union[Dict, predict_response_model]:
        """Inference method. Must
        - only take one `payload` argument
        - use the class attribute `predict_response_model` as a type hint"""

        assert self.ready

        return {}

    def bio(self) -> Union[Dict, bio_response_model]:
        """Placeholder for optional, customizable model meta data. Ideally the `model_card` info
        from a neptune model version entry. Must
        - take no arguments"""

        pass
