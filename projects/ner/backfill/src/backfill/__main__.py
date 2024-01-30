"""Main pipeline."""

# Standard Library
import json
import logging

# 3rd party libraries
import apache_beam as beam

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.base.pydantic import cast
from onclusiveml.data.beam.settings import PipelineSettings
from onclusiveml.data.beam.transforms import MachineLearningEnrichment
from onclusiveml.data.beam.transforms.io.kafka import KafkaConsume, KafkaProduce
from onclusiveml.data.beam.transforms.io.kafka.settings import (
    KafkaConsumerSettings,
    KafkaProducerSettings,
)

# Source
from src.settings import get_settings


def run_beam_pipeline(settings: OnclusiveBaseSettings) -> None:
    """Runs beam pipeline."""
    logging.getLogger().setLevel(logging.INFO)

    flink_options = cast(settings, PipelineSettings).to_pipeline_options()

    consumer = cast(settings, KafkaConsumerSettings)
    producer = cast(settings, KafkaProducerSettings)

    with beam.Pipeline(options=flink_options) as p:
        _ = (
            p
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
                in_keys=[
                    "content",
                    "language",
                ],  # NOTE: Other models parameters go here as kwargs
                api_key=settings.api_key,
                namespace=settings.namespace,
                version=settings.version,
            )
            | "Write To Kafka"
            >> KafkaProduce(
                topic=settings.target_topic, producer_config=producer.config
            )
        )

        result = p.run()
        result.wait_until_finish()

    logging.info("Pipeline execution completed.")


if __name__ == "__main__":
    print(get_settings())
    run_beam_pipeline(get_settings())
