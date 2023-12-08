"""Served model."""

# Standard Library
from logging import getLogger
from typing import Dict, Union

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.serve.server_models import (
    ProtocolV1RequestModel,
    ProtocolV1ResponseModel,
    ServedModelBioModel,
)


class ServedModel(object):
    """A wrapper class.

    Brings in any machine learning model into the ModelServer serving utility
    class for serving ML predictions via REST.
    Roughly follows the kserve.Model implementation.
    """

    predict_request_model: BaseModel = ProtocolV1RequestModel
    predict_response_model: BaseModel = ProtocolV1ResponseModel
    bio_response_model: BaseModel = ServedModelBioModel

    def __init__(self, name: str) -> None:

        self.name = name
        self.ready = False

    def load(self) -> None:
        """Loading the model artifacts and readying the model for inference.

        After calling this method, the model needs to be ready for inference.
        """
        self.ready = True
        # access and attach the uvicorn server loggers
        self.uvicorn_access_logger = getLogger("uvicorn.access")
        self.uvicorn_error_logger = getLogger("uvicorn.error")

    def is_ready(self) -> bool:
        """Customizable readyness probe backend."""
        return self.ready

    def predict(
        self, payload: predict_request_model
    ) -> Union[Dict, predict_response_model]:
        """Inference method.

        Must:
            - only take one `payload` argument
            - use the class attribute `predict_response_model` as a type hint
            - return either an instance of the `predict_response_model` or a dictionary compatible
                with the pydantic constructor utility `predict_response_model.from_dict`
        """
        assert self.ready
        return {}

    def bio(self) -> Union[Dict, bio_response_model]:
        """Placeholder for optional, customizable model meta data.

        Ideally the `model_card` info from a neptune model version entry. Must:
            - take no arguments
            - return either an instance of the `bio_response_model` or a dictionary compatible
            with the pydantic constructor utility `bio_response_model.from_dict`
        """
        return self.bio_response_model(name=self.name)
