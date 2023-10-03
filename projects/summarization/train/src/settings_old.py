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
class TrackedSumModelSpecs(TrackedModelSpecs):
    """Tracked summarization model specs."""

    project: str = "onclusive/summarization"
    model = "SUM-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):
    """Inputs."""

    sample_documents: List[str] = [""]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SumSettings(TrackedParams):
    """Summarization settings."""

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SumModelParamsEn(TrackedParams):
    """English Summarization model settings."""

    huggingface_pipeline_task: str = "summarization"
    huggingface_model_reference: str = "Yale-LILY/brio-cnndm-uncased"

    sum_settings: SumSettings = SumSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
        
        
class SumModelParamsFrDe(TrackedParams):
    """French/German Summarization model settings."""

    huggingface_pipeline_task: str = "summarization"
    huggingface_model_reference: str = "ctu-aic/mbart25-multilingual-summarization-multilarge-cs"

    sum_settings: SumSettings = SumSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
        

class SumModelParamsEs(TrackedParams):
    """Spanish Summarization model settings."""

    huggingface_pipeline_task: str = "summarization"
    huggingface_model_reference: str = "knkarthick/MEETING_SUMMARY"

    sum_settings: SumSettings = SumSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
        
        
class SumModelParamsCa(TrackedParams):
    """Catalan Summarization model settings."""

    huggingface_pipeline_task: str = "summarization"
    huggingface_model_reference: str = "ELiRF/NASCA"

    sum_settings: SumSettings = SumSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SumModelParamsIt(TrackedParams):
    """Italian Summarization model settings."""

    huggingface_pipeline_task: str = "summarization"
    huggingface_model_reference: str = "morenolq/bart-it-fanpage"

    sum_settings: SumSettings = SumSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8" 


class TrackedSumModelCard(TrackedModelCard):
    """The model cards for the model of the multilingual Summarization ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: SumModelParams = SumModelParams()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "sum_model_artifacts")
    logging_level: str = "INFO"

    en_model_subdirectory: str = "/en_sum"
    frde_model_subdirectory: str = "/frde_sum"
    es_model_subdirectory: str = "/es_sum"
    ca_model_subdirectory: str = "/ca_sum"
    it_model_subdirectory: str = "/it_sum"
    
    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"