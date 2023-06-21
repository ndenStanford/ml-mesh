# Internal libraries
from onclusiveml.serving.rest import ServingParams
from onclusiveml.serving.rest.serve import ModelServer

# Source
from src.served_model import KeywordsServedModel
from src.serving_params import ServedModelParams


if __name__ == "__main__":

    served_model_params = ServedModelParams()
    serving_params = ServingParams()

    keywords_served_model = KeywordsServedModel(served_model_params=served_model_params)

    model_server = ModelServer(
        configuration=serving_params, model=keywords_served_model
    )

    model_server.serve()
