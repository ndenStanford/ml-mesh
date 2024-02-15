"""Settings."""

# 3rd party libraries
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

    entity_linking_prod: EntityLinkingProdSettings
    entity_linking_stage: EntityLinkingStageSettings
    NER_prod: NERProdSettings
    NER_stage: NERStageSettings


def get_settings() -> Settings:
    """Get the settings."""
    entity_linking_prod = EntityLinkingProdSettings()
    entity_linking_stage = EntityLinkingStageSettings()
    NER_prod = NERProdSettings()
    NER_stage = NERStageSettings()

    return Settings(
        entity_linking_prod=entity_linking_prod,
        entity_linking_stage=entity_linking_stage,
        NER_prod=NER_prod,
        NER_stage=NER_stage,
    )
