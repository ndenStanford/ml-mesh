"""Settings."""

# Standard Library
import os

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackingSettings,
)


# --- settings classes
class TrackedEntityLinkingModelSpecs(TrackedModelSettings):
    """Tracked entity-linking model settings."""

    project: str = "onclusive/entity-linking"
    model: str = "EL-TRAINED"


class EntityLinkingSettings(TrackingSettings):
    """Entity linking settings."""


class EntityLinkingModelParams(TrackingSettings):
    """Entity linking Model parameters."""

    repo: str = "wannaphong/BELA"
    checkpoint_name: str = "wiki"
    index_filename: str = "index.txt"

    entity_linking_settings: EntityLinkingSettings = EntityLinkingSettings()


class TrackedEntityLinkingBaseModelCard(TrackedModelCard):
    """The model card for the base model of the EL ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: EntityLinkingModelParams = EntityLinkingModelParams()
    # model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "entity_linking_model_artifacts")
    local_cache_dir: str = os.path.join(".", "entity_linking_model_cache")
    logging_level: str = "INFO"
