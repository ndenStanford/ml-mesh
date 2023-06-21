# Internal libraries
from onclusiveml.serving.rest.serve import ModelServer, ServingParams

# Source
from src.served_model import ServedKeywordsModel
from src.serving_params import ServedModelParams


def get_model_server() -> ModelServer:
    """Utility method for prepping a fully configured model server instance ready to serve."""
    # initialize model
    served_model_params = ServedModelParams()
    keywords_served_model = ServedKeywordsModel(served_model_params=served_model_params)
    # initialize model server
    serving_params = ServingParams()
    model_server = ModelServer(
        configuration=serving_params, model=keywords_served_model
    )

    return model_server


if __name__ == "__main__":
    model_server = get_model_server()
    # launch server process(es)
    model_server.serve()
