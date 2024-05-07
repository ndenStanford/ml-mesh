"""Main."""

# Internal libraries
# from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer, ServingParams

# Source
from src.serve.served_model import SummarizationServedModel
from src.settings import get_settings


def get_model_server() -> ModelServer:
    """Instanciates model server.

    Args:
        settings (BaseSettings): application settings.
    """
    serving_params = ServingParams()
    model_server = ModelServer(
        configuration=serving_params, model=SummarizationServedModel()
    )
    print(settings.model_name)
    return model_server


settings = get_settings()
model_server = get_model_server()

if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
