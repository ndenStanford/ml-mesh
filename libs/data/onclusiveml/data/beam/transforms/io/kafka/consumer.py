"""Consumer"""

# Standard Library
import json
import logging
from typing import Any, Dict, Iterable, List, Mapping

# 3rd party libraries
from apache_beam import Create, DoFn, ParDo, PCollection, PTransform
from kafka import KafkaConsumer

# Internal libraries
from onclusiveml.data.beam.exceptions import (
    EmptyConsumerException,
    KafkaConsumerException,
)


class KafkaConsume(PTransform):
    """A :class:`~apache_beam.transforms.ptransform.PTransform` for reading from an Apache Kafka topic. This is a streaming
    Transform that never returns. The transform uses `KafkaConsumer` from the
    `kafka` python library.

    It outputs a :class:`~apache_beam.pvalue.PCollection` of
    ``key-values:s``, each object is a Kafka message in the form (msg-key, msg)

    Args:
        consumer_config (dict): the kafka consumer configuration. The topic to
            be subscribed to should be specified with a key called 'topic'. The
            remaining configurations are those of `KafkaConsumer` from the
            `kafka` python library.
        value_decoder (function): Optional function to decode the consumed
            message value. If not specified, "bytes.decode" is used by default.
            "bytes.decode" which assumes "utf-8" encoding.

    Examples:
        Consuming from a Kafka Topic `notifications` ::

            import apache_beam as beam
            from apache_beam.options.pipeline_options import PipelineOptions
            from onclusiveml.data.beam.transforms.io import kafka

            consumer_config = {"bootstrap_servers": "localhost:9092",
                               "group_id": "notification_consumer_group"}

            with beam.Pipeline(options=PipelineOptions()) as p:
                notifications = p | "Reading messages from Kafka" >> kafka.KafkaConsume(
                    "topic": "notifications",
                    consumer_config=consumer_config,
                    value_decoder=bytes.decode,  # optional
                )
                notifications | 'Writing to stdout' >> beam.Map(print)

        The output will be something like ::

            ("device 1", {"status": "healthy"})
            ("job #2647", {"status": "failed"})

        Where the first element of the tuple is the Kafka message key and the second element is the Kafka message being passed through the topic
    """

    def __init__(
        self, topic: str, consumer_config: Dict, value_decoder=None, **kwargs: Mapping
    ):
        """Initializes ``KafkaConsume``"""
        super(KafkaConsume, self).__init__()
        self._consumer_args = dict(
            topic=topic,
            consumer_config=consumer_config,
            value_decoder=value_decoder,
        )

    def expand(self, pcoll: PCollection) -> PCollection:
        return pcoll | Create([self._consumer_args]) | ParDo(_ConsumeKafkaTopic())


class _ConsumeKafkaTopic(DoFn):
    """Internal ``DoFn`` to read from Kafka topic and return messages"""

    def process(self, consumer_args: Dict):  # type: ignore
        """Process beam do fn."""
        consumer_config = consumer_args.pop("consumer_config")
        topic = consumer_args.pop("topic")
        value_decoder = consumer_args.pop("value_decoder") or bytes.decode
        consumer = KafkaConsumer(topic, **consumer_config)

        for msg in consumer:
            print("*******")
            print("*******")
            print("*******")
            print(msg)
            print("*******")
            print("*******")
            print("*******")
            try:
                yield msg.key, value_decoder(msg.value)
            except Exception as e:
                raise KafkaConsumerException(topics=[topic], message=msg.error())
