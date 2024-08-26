"""Constants."""

# Internal libraries
from onclusiveml.core.base import OnclusiveEnum


class KafkaProducerCompressionType(str, OnclusiveEnum):
    """Kafka producer compression type."""

    GZIP = "gzip"
    SNAPPY = "snappy"
    LZ4 = "lz4"
    ZSTD = "zstd"


class KafkaConsumerOffset(str, OnclusiveEnum):
    """Kafka consumer offset type."""

    EARLIEST = "earliest"
    LATEST = "latest"
