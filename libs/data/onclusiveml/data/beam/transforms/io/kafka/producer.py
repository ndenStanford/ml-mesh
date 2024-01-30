"""Kafka produce."""

# Standard Library
import json
from typing import Dict, Generator, List, Optional, Tuple

# 3rd party libraries
from apache_beam import Create, DoFn, ParDo, PCollection, PTransform
from kafka import KafkaProducer

# Internal libraries
from onclusiveml.data.beam.exceptions import KafkaProducerException
from onclusiveml.data.beam.transforms.io.kafka.settings import (
    KafkaProducerSettings,
)


class KafkaProduce(PTransform):
    """A :class:`~apache_beam.transforms.ptransform.PTransform` for pushing messages
        into an Apache Kafka topic. This class expects a tuple with the first element being the message key
        and the second element being the message. The transform uses `KafkaProducer`
        from the `kafka` python library.

        Args:
            topic: Kafka topic to publish to
            servers: list of Kafka servers to listen to

        Examples:
            Examples:
            Pushing message to a Kafka Topic `notifications` ::

                from __future__ import print_function
                import apache_beam as beam
                from apache_beam.options.pipeline_options import PipelineOptions
                from onclusiveml.data.beam.transforms.io import kafka

                with beam.Pipeline(options=PipelineOptions()) as p:
                    notifications = ( p
                                     | "Creating data" >> beam.Create([('dev_1', '{"device": "0001", status": "healthy"}')])
                                     | "Pushing messages to Kafka" >> kafka.KafkaProduce(
                                            topic='notifications',
                                            producer_config={
                                                "bootstrap_servers": "localhost:9092"
                                            }
                                        )
    3
            The output will be something like ::

                ("dev_1", '{"device": "0001", status": "healthy"}')

            Where the key is the Kafka topic published to and the element is the Kafka message produced
    """

    def __init__(self, topic: str, producer_config: Dict):
        """Initializes ``KafkaProduce``."""
        super(KafkaProduce, self).__init__()
        self._producer_args = dict(topic=topic, producer_config=producer_config)

    def expand(self, pcoll: PCollection) -> PCollection:
        """Expand tranform."""
        return pcoll | ParDo(_ProduceKafkaMessage(**self._producer_args))


class _ProduceKafkaMessage(DoFn):
    """Internal ``DoFn`` to publish message to Kafka topic"""

    def __init__(self, topic: str, producer_config: Dict, *args, **kwargs):
        super(_ProduceKafkaMessage, self).__init__(*args, **kwargs)
        self.topic = topic
        self.producer_config = producer_config

    def start_bundle(self) -> None:
        print(self.producer_config)
        self._producer = KafkaProducer(**self.producer_config)

    def finish_bundle(self) -> None:
        self._producer.close()

    def process(self, element):  # type: ignore
        """Process transform."""
        try:
            self._producer.send(
                self.topic, json.dumps(element[1]).encode(), key=element[0]
            )
            yield element
        except Exception as e:
            raise KafkaProducerException(topic=self.topic)
