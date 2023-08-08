# Standard Library
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.serve import ServedModel
from onclusiveml.syndicate.datasketch import LshHandler

# Source
# from src.serve.params import ServedModelArtifacts
from src.serve.server_models import (
    BioResponseModel,
    PredictRequestModel,
    PredictResponseModel,
)


class ServedLshModel(ServedModel):

    predict_request_model: Type[BaseModel] = PredictRequestModel
    predict_response_model: Type[BaseModel] = PredictResponseModel
    bio_response_model: Type[BaseModel] = BioResponseModel

    def __init__(self) -> None:

        super().__init__(name="lsh")

    def load(self) -> None:
        # load model artifacts into ready CompiledKeyBERT instance
        self.model = LshHandler()
        self.ready = True
        self.model_card = BioResponseModel(model_name="lsh")

    def predict(self, payload: PredictRequestModel) -> PredictResponseModel:
        inputs = payload.inputs

        words = self.model.pre_processing(text=inputs.content, lang=inputs.language)

        shingle_list = self.model.k_shingle(words, k=inputs.shingle_list)
        if len(shingle_list) < 1:
            return PredictResponseModel(signature=None)

        signature = self.model.generate_lsh_signature(
            shingle_list=shingle_list,
            num_perm=inputs.num_perm,
            threshold=inputs.threshold,
        )

        return PredictResponseModel(signature=signature)

    def bio(self) -> BioResponseModel:

        return self.model_card
