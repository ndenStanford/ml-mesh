# type: ignore
"""Model server."""

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer, ServingParams

# Source
from src.serve.model import ServedTopicModel


def get_model_server() -> ModelServer:
    """Utility method for prepping a fully configured model server instance ready to serve."""
    # initialize model
    topic_served_model = ServedTopicModel()
    # initialize model server
    serving_params = ServingParams()

    model_server = ModelServer(configuration=serving_params, model=topic_served_model)
    Instrumentator.enable(model_server, app_name="topic-summarization")

    return model_server


model_server = get_model_server()

if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
