# Internal libraries
from onclusiveml.serving.rest.serve import ModelServer

# Source
from src.keywords_serving_params import KeywordsServingParams
from src.served_keywords_model import ServedKeywordsModel


keywords_serving_params = KeywordsServingParams()

keywords_served_model = ServedKeywordsModel(name="keywords")

keywords_model_server = ModelServer(
    configuration=keywords_serving_params, model=keywords_served_model
)

if __name__ == "__main__":
    keywords_model_server.serve()
