"""Model server getter."""

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer

# Source
from src.serve.model import TranslationModel  # type: ignore[attr-defined]
from src.settings import get_settings


settings = get_settings()


def get_model_server() -> ModelServer:
    """Instanciates model server.

    Args:
        settings (BaseSettings): application settings.
    """
    translation_served_model = TranslationModel()

    model_server = ModelServer(configuration=settings, model=translation_served_model)
    Instrumentator.enable(model_server, app_name=settings.model_name)

    return model_server
