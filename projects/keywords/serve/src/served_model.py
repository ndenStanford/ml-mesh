# Standard Library
import json
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.models.keywords import CompiledKeyBERT
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.server_models import (
    BioResponseModel,
    PredictionExtractedKeyword,
    PredictionOutputDocument,
    PredictRequestModel,
    PredictResponseModel,
)
from src.serving_params import ServedModelParams


class ServedKeywordsModel(ServedModel):

    predict_request_model: Type[BaseModel] = PredictRequestModel
    predict_response_model: Type[BaseModel] = PredictResponseModel
    bio_response_model: Type[BaseModel] = BioResponseModel

    def __init__(self, served_model_params: ServedModelParams):

        self.served_model_params = served_model_params

        super().__init__(name=served_model_params.model_name)

    def load(self) -> None:

        # load model artifacts into ready CompiledKeyBERT instance
        self.model = CompiledKeyBERT.from_pretrained(
            self.served_model_params.model_artifact_directory
        )

        # load model card json file into dict
        with open(self.served_model_params.model_card_file, "r") as json_file:
            self.model_card = json.load(json_file)

        self.ready = True

    def predict(self, payload: PredictRequestModel) -> PredictResponseModel:
        # extract documents and inference call configuration from validated payload
        configuration = payload.configuration
        inputs = payload.inputs

        documents = [input.document for input in inputs]
        # score the model
        predicted_documents = self.model.extract_keywords(
            docs=documents, **configuration.dict()
        )
        # assemble validated response model instance
        predicted_payload_list = []

        for predicted_document in predicted_documents:

            predicted_document_list = []

            for extracted_keyword_token, extracted_keyword_score in predicted_document:

                predicted_document_list.append(
                    PredictionExtractedKeyword(
                        keyword_token=extracted_keyword_token,
                        keyword_score=extracted_keyword_score,
                    )
                )

            predicted_document_model = PredictionOutputDocument(
                predicted_document=predicted_document_list
            )

            predicted_payload_list.append(predicted_document_model)

        return PredictResponseModel(outputs=predicted_payload_list)

    def bio(self) -> BioResponseModel:

        return BioResponseModel(model_name=self.name, model_card=self.model_card)
