"""Settings."""

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
class TrackedSentModelSpecs(TrackedModelSpecs):
    """Tracked sentiment model."""

    project: str = "onclusive/sent"  # TODO: use sentiment project
    model = "SEN-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):
    """Sentiment input parameters."""

    sample_documents: List[str] = [""]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SentSettings(TrackedParams):
    """Sentiment settings."""

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SentModelParams(TrackedParams):
    """Sentiment Model parameters."""

    huggingface_pipeline_task: str = "sentiment-analysis"
    huggingface_model_reference: str = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

    sent_settings: SentSettings = SentSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class TrackedSentBaseModelCard(TrackedModelCard):
    """The model card for the base model of the Sent ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: SentModelParams = SentModelParams()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "sent_model_artifacts")
    logging_level: str = "INFO"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
