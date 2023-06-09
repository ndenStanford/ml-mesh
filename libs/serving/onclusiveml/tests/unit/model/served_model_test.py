# Internal libraries
from onclusiveml.serving.rest.models import ProtocolV1RequestModel
from onclusiveml.serving.rest.served_model import ServedModel


def test_served_model():

    served_model = ServedModel()
    # base class `load` behaviour
    assert served_model.ready is not True
    assert served_model.is_ready() is not True

    served_model.load()

    assert served_model.ready is True
    assert served_model.is_ready() is True
    # `predict` stump
    request_arg = ProtocolV1RequestModel(instances=[1, 2])
    some_arg = 1
    some_kwarg = 2
    served_model.predict(request_arg, some_arg, some_kwarg=some_kwarg)
