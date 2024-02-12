"""Pipeline definition."""

# Standard Library
import json

# 3rd party libraries
import apache_beam as beam

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.base.pydantic import cast
from onclusiveml.data.beam.transforms import MachineLearningEnrichment
from onclusiveml.data.beam.transforms.io.kafka import KafkaConsume, KafkaProduce
from onclusiveml.data.beam.transforms.io.kafka.settings import (
    KafkaConsumerSettings,
    KafkaProducerSettings,
)


def get_pipeline(root: beam.Pipeline, settings: OnclusiveBaseSettings) -> beam.Pipeline:
    """Returns beam pipeline."""
    consumer = cast(settings, KafkaConsumerSettings)
    producer = cast(settings, KafkaProducerSettings)

    pipeline = (
        root
        | "Read From Kafka"
        >> KafkaConsume(
            topic=settings.source_topic,
            consumer_config=consumer.config,
        )
        | "Decode" >> beam.Map(lambda x: (x[0], json.loads(x[1])))
        | f"Enrichment: {settings.namespace}"
        >> MachineLearningEnrichment(
            host=settings.host,
            secure=settings.secure,
            in_keys=["content"],  # NOTE: Other models parameters go here as kwargs
            api_key=settings.api_key,
            namespace=settings.namespace,
            version=settings.version,
        )
        | "Write To Kafka"
        >> KafkaProduce(topic=settings.target_topic, producer_config=producer.config)
    )

    return pipeline
