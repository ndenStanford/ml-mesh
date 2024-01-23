"""Kafka io test."""

# 3rd party libraries
import apache_beam as beam
import pytest
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

# Internal libraries
from onclusiveml.data.beam.transforms.io.kafka import KafkaConsume, KafkaProduce


@pytest.mark.parametrize(
    "topic, producer_config, data",
    [
        (
            "test",
            {"socket.timeout.ms": 10, "message.timeout.ms": 10},
            [("id", {"key": "data"})],
        )
    ],
)
def test_kafka_produce_without_broker(topic, producer_config, data):
    """Test kafka produce."""
    with TestPipeline() as pipeline:
        result = (
            pipeline
            | "Start" >> beam.Create(data)
            | "Do" >> KafkaProduce(topic=topic, producer_config=producer_config)
        )
        assert_that(result, equal_to([("id", {"key": "data"})]))


@pytest.mark.parametrize(
    "topic, consumer_config", [("test", {"group.id": "notification_consumer_group"})]
)
def test_kafka_consumer(topic, consumer_config):
    """Test kafka comsume."""
    with TestPipeline() as pipeline:
        _ = pipeline | "Do" >> KafkaConsume(
            consumer_config=consumer_config, topics=["beam"], timeout=0.01, test=True
        )
