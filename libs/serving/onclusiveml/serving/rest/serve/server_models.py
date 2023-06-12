# Standard Library
from typing import Any, List

# 3rd party libraries
from pydantic import BaseModel


class ReadinessProbeResponse(BaseModel):

    ready: bool = True


class LivenessProbeResponse(BaseModel):
    live: bool = True


class ProtocolV1RequestModel(BaseModel):

    instances: List[Any]


class ProtocolV1ResponseModel(BaseModel):

    predictions: List[Any]
