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
class TrackedNERModelSpecs(TrackedModelSettings):
    """Tracked NER model specs."""

    project: str = "onclusive/ner"
    model: str = "NER-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackingSettings):
    """Inputs."""

    sample_documents: List[List[str]] = [
        [
            "Google HQ is in Mountain View, CA",
            "Hitchhiking onto the Gulf Stream, adult sea turtles often end up as far north as "
            + "Cape Cod in their migratory travels.",
            "Nesting season started March 1, so female loggerhead, green and leatherback sea "
            + "turtles will be visiting Jupiter beaches to lay their eggs.",
            "Check out Loggerhead Marinelife Center for a close look at sea turtles.",
        ],
        [
            "Google 本社はカリフォルニア州マウンテンビューにあります",
            "メキシコ湾流でヒッチハイクをする大人のウミガメは、回遊の旅の途中で北のケープコッドまで到達することがよくあります。",
            "런던과 샌프란시스코에 가족이 있어요",
            "바다거북을 가까이서 관찰하려면 Loggerhead Marinelife Center를 확인하세요.",
        ],
    ]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class NERSettings(TrackingSettings):
    """NER settings."""

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class NERModelParams(TrackingSettings):
    """Ner model settings."""

    ner_settings: NERSettings = NERSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class NERModelParamsBase(NERModelParams):
    """Dslim NER model."""

    huggingface_pipeline_task: str = "token-classification"
    huggingface_model_reference: str = "dslim/bert-base-NER"


class NERModelParamsKJ(NERModelParams):
    """Korean/Japanese NER model."""

    huggingface_pipeline_task_kj: str = "token-classification"
    huggingface_model_reference_kj: str = (
        "Davlan/distilbert-base-multilingual-cased-ner-hrl"
    )


class TrackedNERBaseModelCard(TrackedModelCard):
    """The model card for the base model of the NER ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    ner_model_params_base: NERModelParamsBase = NERModelParamsBase()
    ner_model_params_kj: NERModelParamsKJ = NERModelParamsKJ()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "ner_model_artifacts")
    logging_level: str = "INFO"

    kj_model_subdirectory: str = "/korean_japanese_ner"
    base_model_subdirectory: str = "/base_ner"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
