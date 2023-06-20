# Source
from src.keywords_serving_params import KeywordsServedModelParams
from src.served_keywords_model import ServedKeywordsModel


def test_served_keywords_model__init__(test_model_name):

    served_keywords_model_params = KeywordsServedModelParams(model_name=test_model_name)
    ServedKeywordsModel(served_model_params=served_keywords_model_params)
