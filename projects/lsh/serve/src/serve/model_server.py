"""Model server."""

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer, ServingParams

# Source
from src.serve.served_model import ServedLshModel


def get_model_server() -> ModelServer:
    """Utility method for retrieving a fully configured model server instance.

    Returns:
        ModelServer: A model server instance.
    """
    # initialize model
    lsh_served_model = ServedLshModel()
    # initialize model server
    serving_params = ServingParams()

    model_server = ModelServer(configuration=serving_params, model=lsh_served_model)
    Instrumentator.enable(model_server, app_name="lsh")

    return model_server


model_server = get_model_server()

if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
