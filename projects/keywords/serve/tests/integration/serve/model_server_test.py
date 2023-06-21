# Source
from src.model_server import get_model_server
from src.served_model import ServedKeywordsModel


def test_get_model_server():

    model_server = get_model_server()

    assert isinstance(model_server.model, ServedKeywordsModel)
    assert not model_server.model.is_ready()
