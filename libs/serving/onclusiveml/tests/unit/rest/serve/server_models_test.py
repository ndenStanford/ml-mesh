# 3rd party libraries
from served_model_test import TestPrediction, TestRecord

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ProtocolV1RequestModel,
    ProtocolV1ResponseModel,
    ReadinessProbeResponse,
    ServedModelBioModel,
)


def test_readiness_probe_response_model():

    ReadinessProbeResponse().dict() == {"ready": True}


def test_liveness_probe_response_model():

    LivenessProbeResponse().dict() == {"live": True}


def test_ml_protocol_v1_request_model():

    ProtocolV1RequestModel(
        instances=[TestRecord(number_of_legs=0), TestRecord(number_of_legs=1)]
    )


def test_ml_protocol_v1_response_model():

    ProtocolV1ResponseModel(
        predictions=[TestPrediction(animal="snake"), TestPrediction(animal="flamingo")]
    )


def test_ml_bio_response_model(test_model_name):

    ServedModelBioModel(name=test_model_name)
