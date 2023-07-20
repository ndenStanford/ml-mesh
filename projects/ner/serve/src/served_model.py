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
        # content and configuration from payload
        configuration = payload.configuration
        inputs = payload.inputs

        # score the model
        entities = self.model.extract_entities(
            sentences=inputs.content, **configuration.dict()
        )

        entities_list = []
        for entity in entities:

            entities_list.append(
                PredictionExtractedEntity(
                    entity_type=entity["entity_type"],
                    entity_text=entity["entity_text"],
                    score=entity["score"],
                    sentence_index=entity["sentence_index"],
                    start=entity["start"],
                    end=entity["end"],
                )
            )

            entity_model = PredictionOutputContent(predicted_content=entities_list)

        return PredictResponseModel(outputs=entity_model)

    def bio(self) -> BioResponseModel:

        return BioResponseModel(model_name=self.name, model_card=self.model_card)
