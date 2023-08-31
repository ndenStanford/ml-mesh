"""Model server."""

# Internal libraries
from onclusiveml.serving.rest.serve import ModelServer, ServingParams

# Source
from src.serve.served_model import ServedLshModel


def get_model_server() -> ModelServer:
    """Utility method for prepping a fully configured model server instance ready to serve."""
    # initialize model
    lsh_served_model = ServedLshModel()
    # initialize model server
    serving_params = ServingParams()
    model_server = ModelServer(configuration=serving_params, model=lsh_served_model)

    return model_server


if __name__ == "__main__":
    model_server = get_model_server()
    # launch server process(es)
    model_server.serve()
