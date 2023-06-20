# Standard Library
import os
from typing import List

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedParams,
)


# --- settings classes
class TrackedNERModelSpecs(TrackedModelSpecs):
    project: str = "onclusive/ner"
    model = "NER-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):

    sample_documents: List[str]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class NERModelParams(TrackedParams):
    huggingface_pipeline_task: str = "token-classification"
    huggingface_model_reference: str = "dslim/bert-base-NER"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class TrackedNERBaseModelCard(TrackedModelCard):
    """The model card for the base model of the NER ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: NERModelParams = NERModelParams()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "ner_model_artifacts")
    logging_level: str = "INFO"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
