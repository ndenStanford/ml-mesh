"""Model server."""

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer, ServingParams

# Source
from src.serve.served_model import ServedLshModel


# initialize model
lsh_served_model = ServedLshModel()
# initialize model server
serving_params = ServingParams()
model_server = ModelServer(configuration=serving_params, model=lsh_served_model)
Instrumentator.enable(model_server, app_name="lsh")


if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
