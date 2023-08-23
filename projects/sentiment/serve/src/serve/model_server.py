# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer, ServingParams

# Source
from src.serve.params import ServedModelArtifacts
from src.serve.served_model import ServedSentModel


def get_model_server() -> ModelServer:
    """
    Utility method for prepping a fully configured model server instance ready to serve.

    Returns:
        ModelServer: Configured model server instance
    """
    # initialize model
    served_model_artifacts = ServedModelArtifacts(remove_model_prefix=True)
    sent_served_model = ServedSentModel(served_model_artifacts=served_model_artifacts)
    # initialize model server
    serving_params = ServingParams()
    model_server = ModelServer(configuration=serving_params, model=sent_served_model)
    Instrumentator.enable(model_server, app_name="sentiment")

    return model_server


if __name__ == "__main__":
    model_server = get_model_server()
    # launch server process(es)
    model_server.serve()
