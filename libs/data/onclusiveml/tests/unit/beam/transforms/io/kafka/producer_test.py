"""Producer test."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import apache_beam as beam
import pytest
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to
from kafka import KafkaProducer
from kafka.client_async import KafkaClient

# Internal libraries
from onclusiveml.data.beam.transforms.io.kafka import KafkaProduce


@pytest.mark.parametrize(
    "topic, producer_config, data",
    [
        (
            "foo",
            {},
            [("id", {"key": "data"})],
        )
    ],
)
@patch.object(KafkaProducer, "send")
@patch.object(KafkaClient, "check_version")
def test_kafka_produce_without_broker(
    kafka_client, kafka_send, topic, producer_config, data
):
    """Test kafka produce."""
    kafka_client.return_value = (0, 11)

    with TestPipeline() as pipeline:
        result = (
            pipeline
            | "Start" >> beam.Create(data)
            | "Do" >> KafkaProduce(topic=topic, producer_config=producer_config)
        )
        assert_that(result, equal_to([("id", {"key": "data"})]))
