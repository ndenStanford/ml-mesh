"""Settings."""

# Standard Library
from functools import lru_cache

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.data.beam.settings import (
    EnrichmentPipelineSettings,
    PipelineSettings,
)
from onclusiveml.data.beam.transforms.io.kafka.settings import (
    KafkaConsumerSettings,
    KafkaProducerSettings,
)


class GlobalSettings(
    EnrichmentPipelineSettings,
    PipelineSettings,
    KafkaProducerSettings,
    KafkaConsumerSettings,
):
    """Global settings."""

    source_topic: str
    target_topic: str
    timeout: float = 0.01
    test: bool = False


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
