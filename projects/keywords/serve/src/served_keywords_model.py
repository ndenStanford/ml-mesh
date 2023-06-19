# Standard Library
import json
import os
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.models.keywords import CompiledKeyBERT
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.keywords_serving_params import KeywordsServedModelParams
from src.served_keywords_data_models import (
    KeywordsBioResponseModel,
    KeywordsPredictionExtractedKeyword,
    KeywordsPredictionOutputDocument,
    KeywordsPredictRequestModel,
    KeywordsPredictResponseModel,
)


class ServedKeywordsModel(ServedModel):

    predict_request_model: Type[BaseModel] = KeywordsPredictRequestModel
    predict_response_model: Type[BaseModel] = KeywordsPredictResponseModel
    bio_response_model: Type[BaseModel] = KeywordsBioResponseModel

    served_model_params: KeywordsServedModelParams = KeywordsServedModelParams()

    def load(self) -> None:
        # load and attach model_card attribute
        model_card_path = os.path.join(
            self.served_model_params.model_artifact_directory,
            self.served_model_params.model_card,
        )

        with open(model_card_path, "r") as model_card_json_file:
            self.model_card = json.load(model_card_json_file)
        # load model artifacts into ready CompiledKeyBERT instance
        self.model = CompiledKeyBERT.from_pretrained(
            self.served_model_params.model_artifact_directory
        )

        self.ready = True

    def predict(
        self, payload: KeywordsPredictRequestModel
    ) -> KeywordsPredictResponseModel:

        # extract documents and inference call configuration from validated payload
        inference_configuration = payload.inference_configuration
        inference_inputs = payload.inference_inputs

        documents = [input.document for input in inference_inputs]

        # score the model
        predicted_documents = self.model.extract_keywords(
            docs=documents, **inference_configuration.dict()
        )

        # assemble validated response model instance
        predicted_payload_list = []

        for predicted_document in predicted_documents:

            predicted_document_list = []

            for extracted_keyword_token, extracted_keyword_score in predicted_document:

                predicted_document_list.append(
                    KeywordsPredictionExtractedKeyword(
                        keyword_token=extracted_keyword_token,
                        keyword_score=extracted_keyword_score,
                    )
                )

            predicted_document_model = KeywordsPredictionOutputDocument(
                predicted_document=predicted_document_list
            )

            predicted_payload_list.append(predicted_document_model)

        return KeywordsPredictResponseModel(inference_outputs=predicted_payload_list)

    def bio(self) -> KeywordsBioResponseModel:

        return KeywordsBioResponseModel(
            name=self.name, tracked_keywords_model_card=self.model_card
        )
