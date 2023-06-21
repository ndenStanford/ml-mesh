# Source
from src.served_model import ServedKeywordsModel
from src.serving_params import ServedModelParams


def test_served_keywords_model__init__(test_model_name):

    served_model_params = ServedModelParams(model_name=test_model_name)
    ServedKeywordsModel(served_model_params=served_model_params)


def test_served_keywords_model_load(test_model_name):

    served_model_params = ServedModelParams(model_name=test_model_name)
    served_keywords_model = ServedKeywordsModel(served_model_params=served_model_params)

    assert not served_keywords_model.is_ready()

    served_keywords_model.load()

    assert served_keywords_model.is_ready()
