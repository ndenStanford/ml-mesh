# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer, ServingParams

# Source
from src.serve.params import ServedModelArtifacts
from src.serve.served_model import ServedKeywordsModel


def get_model_server() -> ModelServer:
    """Utility method for prepping a fully configured model server instance ready to serve."""
    # initialize model
    served_model_artifacts = ServedModelArtifacts()
    keywords_served_model = ServedKeywordsModel(
        served_model_artifacts=served_model_artifacts
    )
    # initialize model server
    serving_params = ServingParams()
    model_server = ModelServer(
        configuration=serving_params, model=keywords_served_model
    )
    Instrumentator.enable(model_server, app_name="keywords")

    return model_server


if __name__ == "__main__":
    model_server = get_model_server()
    # launch server process(es)
    model_server.serve()
