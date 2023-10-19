"""Server models tests."""

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ProtocolV1RequestModel,
    ProtocolV1ResponseModel,
    ReadinessProbeResponse,
    ServedModelBioModel,
)


def test_readiness_probe_response_model():
    """Tests the initialization and structure of the ReadinessProbeResponse data model."""
    ReadinessProbeResponse().dict() == {"ready": True}


def test_liveness_probe_response_model():
    """Tests the initialization and structure of the LivenessProbeResponse data model."""
    LivenessProbeResponse().dict() == {"live": True}


def test_ml_protocol_v1_request_model(get_test_record):
    """Tests the initialization of the ProtocolV1RequestModel data model."""
    ProtocolV1RequestModel(
        instances=[get_test_record(number_of_legs=0), get_test_record(number_of_legs=1)]
    )


def test_ml_protocol_v1_response_model(get_test_prediction):
    """Tests the initialization of the ProtocolV1ResponseModel data model."""
    ProtocolV1ResponseModel(
        predictions=[
            get_test_prediction(animal="snake"),
            get_test_prediction(animal="flamingo"),
        ]
    )


def test_ml_bio_response_model(test_model_name):
    """Tests the initialization of the ServedModelBioModel data model."""
    ServedModelBioModel(name=test_model_name)
