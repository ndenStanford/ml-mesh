"""Kafka settings."""

# Standard Library
from typing import Dict, Optional

# 3rd party libraries
from pydantic import Field, SecretStr

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.data.kafka.constants import (
    KafkaConsumerOffset,
    KafkaProducerCompressionType,
)


class KafkaBaseSettings(OnclusiveBaseSettings):
    """Kafka base settings."""

    bootstrap_servers: str = Field(alias="bootstrap.servers")
    security_protocol: Optional[str] = Field(None, alias="security.protocol")
    sasl_mechanism: Optional[str] = Field(None, alias="sasl.mechanism")
    sasl_username: Optional[str] = Field(None, alias="sasl.username")
    sasl_password: Optional[SecretStr] = Field(None, alias="sasl.password")

    @property
    def config(self) -> Dict:
        """Kafka config."""
        return self.dict(exclude_none=True, by_alias=True)


class KafkaProducerSettings(KafkaBaseSettings):
    """Kafka producer settings."""

    compression_type: KafkaProducerCompressionType = Field(
        KafkaProducerCompressionType.NONE, alias="compression.type"
    )
    socket_timeout_ms: Optional[int] = Field(None, alias="socket.timeout.ms")
    message_timeout_ms: Optional[int] = Field(None, alias="message.timeout.ms")


class KafkaConsumerSettings(KafkaBaseSettings):
    """Kafka consumer settings."""

    group_id: str = Field(KafkaConsumerOffset.EARLIEST, alias="group.id")
    auto_offset_reset: str = Field(alias="auto.offset.reset")
