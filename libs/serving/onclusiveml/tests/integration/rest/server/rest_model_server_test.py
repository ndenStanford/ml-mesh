# Internal libraries
from libs.serving.onclusiveml.serving.rest.params import ServingParams
from onclusiveml.serving.rest.serve.model_server import ModelServer


def test_rest_model_server___init__():

    default_serving_params = ServingParams()

    _ = ModelServer(configuration=default_serving_params)


def test_rest_model_server_serve():

    default_serving_params = ServingParams()

    test_model_server = ModelServer(configuration=default_serving_params)

    test_model_server.serve()
