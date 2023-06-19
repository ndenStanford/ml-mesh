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
        self, payload: predict_request_model  # type: ignore[valid-type]
    ) -> predict_response_model:  # type: ignore[valid-type]

        payload_documents = [
            instance.document for instance in payload.instances  # type: ignore[attr-defined]
        ]

        predicted_documents = self.model.extract_keywords(payload_documents)

        print(predicted_documents)

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

        return self.predict_response_model(predictions=predicted_payload_list)

    def bio(self) -> bio_response_model:  # type: ignore[valid-type]

        return self.bio_response_model(
            name=self.name, tracked_keywords_model_card=self.model_card
        )
