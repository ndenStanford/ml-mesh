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
class TrackedSENTModelSpecs(TrackedModelSpecs):
    project: str = "onclusive/sent"
    model = "SEN-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):

    sample_documents: List[str] = [""]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SENTSettings(TrackedParams):
    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SENTModelParams(TrackedParams):
    huggingface_pipeline_task: str = "text-classification"
    huggingface_model_reference: str = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

    sent_settings: SENTSettings = SENTSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class TrackedSENTBaseModelCard(TrackedModelCard):
    """The model card for the base model of the SENT ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: SENTModelParams = SENTModelParams()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "sent_model_artifacts")
    logging_level: str = "INFO"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
