# Standard Library
from typing import Any

# 3rd party libraries
import pydantic

# Internal libraries
from onclusiveml.serving.rest.models import (
    ProtocolV1RequestModel,
    ProtocolV1ResponseModel,
)


class ServedModel(object):
    """A wrapper class for bringing in any machine learning model into the
    - RESTApp
    serving utility class for serving ML predictions via REST.

    Roughly follows the kserve.Model implementation."""

    name: str = "served_model"
    request_model: pydantic.BaseModel = ProtocolV1RequestModel
    response_model: pydantic.BaseModel = ProtocolV1ResponseModel

    def __init__(self) -> None:

        self.ready = False

    def load(self) -> None:
        """Loading the model artifacts and readying the model for inference. After calling this
        method, the model needs to be ready for inference.
        """

        self.ready = True

        pass

    def is_ready(self) -> bool:
        """Customizable readyness probe backend that considers the state of the served model"""

        return self.ready

    def predict(
        self, request: request_model, *args: Any, **kwargs: Any
    ) -> response_model:
        """Inference method."""

        pass

    def bio(self) -> None:
        """Placeholder for optional, customizable model meta data. Ideally the `model_card` info
        from a neptune model version entry."""

        pass
