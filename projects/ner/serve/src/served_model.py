# Standard Library
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.models.ner import CompiledNER
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.server_models import (
    BioResponseModel,
    PredictionExtractedEntity,
    PredictionOutputContent,
    PredictRequestModel,
    PredictResponseModel,
)
from src.serving_params import ServedModelArtifacts


class ServedNERModel(ServedModel):

    predict_request_model: Type[BaseModel] = PredictRequestModel
    predict_response_model: Type[BaseModel] = PredictResponseModel
    bio_response_model: Type[BaseModel] = BioResponseModel

    def __init__(self, served_model_artifacts: ServedModelArtifacts):

        self.served_model_artifacts = served_model_artifacts

        super().__init__(name=served_model_artifacts.model_name)

    def load(self) -> None:

        # load model artifacts into ready CompiledNER instance
        self.model = CompiledNER.from_pretrained(
            self.served_model_artifacts.model_artifact_directory
        )

        # load model card json file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True

    def predict(self, payload: PredictRequestModel) -> PredictResponseModel:
        # extract documents and inference call configuration from validated payload
        configuration = payload.configuration
        inputs = payload.inputs

        # score the model
        predicted_documents = self.model.extract_entities(
            sentences=inputs.content, **configuration.dict()
        )
        # assemble validated response model instance
        predicted_payload_list = []

        for predicted_document in predicted_documents:

            predicted_document_list = []

            for (
                extracted_entity,
                extracted_score,
                extracted_index,
                extracted_word,
                extracted_start,
                extracted_end,
            ) in predicted_document:

                predicted_document_list.append(
                    PredictionExtractedEntity(
                        entity=extracted_entity,
                        score=extracted_score,
                        index=extracted_index,
                        word=extracted_word,
                        start=extracted_start,
                        end=extracted_end,
                    )
                )

            predicted_document_model = PredictionOutputContent(
                predicted_document=predicted_document_list
            )

            predicted_payload_list.append(predicted_document_model)

        return PredictResponseModel(outputs=predicted_payload_list)

    def bio(self) -> BioResponseModel:

        return BioResponseModel(model_name=self.name, model_card=self.model_card)
