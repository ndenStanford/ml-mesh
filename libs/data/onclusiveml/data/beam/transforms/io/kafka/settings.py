"""Kafka settings."""

# Standard Library
from typing import Dict, Optional

# 3rd party libraries
from pydantic import Field, SecretStr

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.data.beam.transforms.io.kafka.constants import (
    KafkaConsumerOffset,
)


class KafkaBaseSettings(OnclusiveBaseSettings):
    """Kafka base settings."""

    bootstrap_servers: str
    security_protocol: Optional[str] = None
    sasl_mechanism: Optional[str] = None
    sasl_username: Optional[str] = None
    sasl_password: Optional[SecretStr] = None

    @property
    def config(self) -> Dict:
        """Kafka config."""
        return self.dict(exclude_none=True, by_alias=True)


class KafkaProducerSettings(KafkaBaseSettings):
    """Kafka producer settings."""

    socket_timeout_ms: Optional[int] = Field(None)
    message_timeout_ms: Optional[int] = Field(None)


class KafkaConsumerSettings(KafkaBaseSettings):
    """Kafka consumer settings."""

    group_id: str = Field(KafkaConsumerOffset.EARLIEST)
    auto_offset_reset: str
