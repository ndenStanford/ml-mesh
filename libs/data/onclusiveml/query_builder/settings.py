"""Settings."""

# Standard Library
from typing import Any, List

# 3rd party libraries
from elasticsearch import Elasticsearch
from pydantic import Field, SecretStr

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings


class ApiSettings(OnclusiveBaseSettings):
    """EL."""

    api_key: SecretStr = Field(default="api_token", exclude=True)
    predict_url: str


class EntityLinkingProdSettings(ApiSettings):
    """EL."""

    predict_url = "https://internal.api.ml.prod.onclusive.com/entity-linking/v1/predict"

    class Config:
        env_prefix = "onclusiveml_data_entity_linking_prod_"


class EntityLinkingStageSettings(ApiSettings):
    """EL."""

    predict_url = (
        "https://internal.api.ml.stage.onclusive.com/entity-linking/v1/predict"
    )

    class Config:
        env_prefix = "onclusiveml_data_entity_linking_stage_"


class NERProdSettings(ApiSettings):
    """NER Prod."""

    predict_url = "https://internal.api.ml.prod.onclusive.com/ner/v1/predict"

    class Config:
        env_prefix = "onclusiveml_data_ner_prod_"


class NERStageSettings(ApiSettings):
    """NER Stage."""

    predict_url = "https://internal.api.ml.stage.onclusive.com/ner/v1/predict"

    class Config:
        env_prefix = "onclusiveml_data_ner_stage_"


class Settings(OnclusiveBaseSettings):
    """Settings."""

    es: Any
    entity_linking_prod: EntityLinkingProdSettings
    entity_linking_stage: EntityLinkingStageSettings
    NER_prod: NERProdSettings
    NER_stage: NERStageSettings
    es_index: List[str]


def get_settings() -> Settings:
    """Get the settings."""
    es = Elasticsearch(
        [
            "https://crawler-prod:GnVjrB5jXgGGzPZHWNRpwWGu4NqTWJsw@search5-client.airpr.com"
        ],
        timeout=30,
        max_retries=10,
        retry_on_timeout=True,
    )

    entity_linking_prod = EntityLinkingProdSettings()
    entity_linking_stage = EntityLinkingStageSettings()
    NER_prod = NERProdSettings()
    NER_stage = NERStageSettings()

    es_index = ["crawler", "crawler-2023.11", "crawler-2023.10", "crawler-2023.09"]

    return Settings(
        es=es,
        es_index=es_index,
        entity_linking_prod=entity_linking_prod,
        entity_linking_stage=entity_linking_stage,
        NER_prod=NER_prod,
        NER_stage=NER_stage,
    )
