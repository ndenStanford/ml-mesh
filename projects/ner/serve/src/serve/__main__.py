"""Model server."""

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.model import ServedNERModel
from src.settings import get_settings


settings = get_settings()
artifacts = ServedModelArtifacts(settings)


# initialize model
ner_served_model = ServedNERModel(served_model_artifacts=artifacts)
# initialize model server
model_server = ModelServer(configuration=settings, model=ner_served_model)
Instrumentator.enable(model_server, app_name=settings.model_name)

if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
