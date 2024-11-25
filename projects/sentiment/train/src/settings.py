"""Settings."""

# Standard Library
import os
from typing import List

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackingSettings,
)


# --- settings classes
class TrackedSentModelSpecs(TrackedModelSettings):
    """Tracked sentiment model settings."""

    project: str = "onclusive/sentiment"
    model: str = "SEN-TRAINED"


class Inputs(TrackingSettings):
    """Sentiment input parameters."""

    sample_documents: List[str] = [""]


class SentSettings(TrackingSettings):
    """Sentiment settings."""


class SentModelParams(TrackingSettings):
    """Sentiment Model parameters."""

    huggingface_pipeline_task: str = "sentiment-analysis"
    huggingface_model_reference: str = "yangheng/deberta-v3-base-absa-v1.1"

    sent_settings: SentSettings = SentSettings()


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
