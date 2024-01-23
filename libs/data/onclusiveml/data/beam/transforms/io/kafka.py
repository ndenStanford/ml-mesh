"""Kafka IO."""

# Standard Library
import json
import logging
from typing import Any, Dict, Iterable, List, Mapping

# 3rd party libraries
from apache_beam import Create, DoFn, ParDo, PCollection, PTransform
from confluent_kafka import KafkaError, Message, Producer

# Internal libraries
from onclusiveml.data.beam.exceptions import (
    EmptyConsumerException,
    KafkaConsumerException,
    KafkaProducerException,
)
from onclusiveml.data.kafka import OnclusiveKakfaConsumer


class KafkaConsume(PTransform):
    """A :class:`~apache_beam.transforms.ptransform.PTransform` for reading from an Apache Kafka topic.

    This is a streaming Transform that never returns. The transform uses `KafkaConsumer` from the
    `kafka` python library. This allows us to define our beam jobs using the native python SDK.
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
            from onclusiveml.data.beam.transforms.io.kafka import KafkaConsume

            consumer_config = {"topic": "notifications",
                               "bootstrap_servers": "localhost:9092",
                               "group_id": "notification_consumer_group"}

            with beam.Pipeline(options=PipelineOptions()) as p:
                notifications = p | "Reading messages from Kafka" >> KafkaConsume(
                    consumer_config=consumer_config,
                    topics=["beam"],
                    timeout=0.01,
                    test=False
                )
                notifications | 'Writing to stdout' >> beam.Map(print)
        The output will be something like ::
            ("device 1", {"status": "healthy"})
            ("job #2647", {"status": "failed"})
        Where the first element of the tuple is the Kafka message key and
        the second element is the Kafka message being passed through the topic.
    """

    def __init__(
        self,
        consumer_config: Dict,
        topics: List[str],
        timeout: float,
        test: bool,
        *args: Iterable,
        **kwargs: Mapping
    ):
        super(KafkaConsume, self).__init__()
        self._consumer_args = dict(
            consumer_config=consumer_config, topics=topics, timeout=timeout, test=test
        )

    def expand(self, pcoll: PCollection) -> PCollection:
        """Expand tranform."""
        return pcoll | Create([self._consumer_args]) | ParDo(_ConsumeKafkaTopic())


class _ConsumeKafkaTopic(DoFn):
    """Internal ``DoFn`` to read from Kafka topic and return messages."""

    def process(self, consumer_args: Dict) -> Any:
        """Process beam do fn."""
        consumer = OnclusiveKakfaConsumer(
            config=consumer_args["consumer_config"],
            topics=consumer_args["topics"],
            timeout=consumer_args["timeout"],
            test=consumer_args["test"],
        )

        try:
            for msg in consumer:
                if msg is None:
                    raise EmptyConsumerException(topics=consumer_args["topics"])
                elif msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        logging.error(
                            "%% %s [%d] reached end at offset %d\n"
                            % (msg.topic(), msg.partition(), msg.offset())
                        )
                    elif msg.error():
                        raise KafkaConsumerException(
                            topics=consumer_args["topics"], message=msg.error()
                        )
                else:
                    consumer.commit(asynchronous=False)
                    yield msg.key().decode("utf-8"), msg.value().decode(
                        "utf-8"
                    )  # TODO: move decoding to a beam step.
        finally:
            consumer.close()


class KafkaProduce(PTransform):
    """A :class:`~apache_beam.transforms.ptransform.PTransform` for pushing messages to a Kafka topic.

    This class expects a tuple with the first element being the message key
    and the second element being the message. The transform uses `KafkaProducer`
    from the `kafka_confluent` python library.

    Args:
        topic (str): Kafka topic to publish to
        servers (List[str]): list of Kafka servers to listen to

    Examples:
        Pushing message to a Kafka Topic `notifications` ::
            from __future__ import print_function
            import apache_beam as beam
            from apache_beam.options.pipeline_options import PipelineOptions
            from onclusiveml.data.beam.transforms.io import kafka
            with beam.Pipeline(options=PipelineOptions()) as p:
                notifications = (p
                                    | "Creating data" >> beam.Create(
                                    [('dev_1', '{"device": "0001", status": "healthy"}')]
                                )
                                    | "Pushing messages to Kafka" >> kafkaio.KafkaProduce(
                                        topic='notifications',
                                        servers="localhost:9092"
                                    )
                                )
                notifications | 'Writing to stdout' >> beam.Map(print)
        The output will be something like ::
            ("dev_1", '{"device": "0001", status": "healthy"}')
        Where the key is the Kafka topic published to and the element is the Kafka message produced.
    """

    def __init__(self, producer_config: Dict, topic: str):
        """Initializes ``KafkaProduce``."""
        super(KafkaProduce, self).__init__()
        self._attributes = dict(topic=topic, producer_config=producer_config)

    def expand(self, pcoll: PCollection) -> PCollection:
        """Expand tranform."""
        return pcoll | ParDo(_ProduceKafkaMessage(self._attributes))


class _ProduceKafkaMessage(DoFn):
    """Internal ``DoFn`` to publish message to Kafka topic."""

    def __init__(self, attributes: Dict, *args: Iterable, **kwargs: Mapping):
        super(_ProduceKafkaMessage, self).__init__(*args, **kwargs)
        self.attributes = attributes

    def start_bundle(self) -> None:
        self._producer = Producer(self.attributes["producer_config"])

    def finish_bundle(self) -> None:
        self._producer.flush()

    def _delivery_report(self, err: KafkaError, msg: Message) -> None:
        """Called once for each message produced.

        Indicate delivery result. Is Triggered by poll() or flush().

        Args:
            err (KafkaError): Kafka error
            msg (Message): Error message
        """
        if err:
            logging.error("Message delivery failed: {}".format(err))
        else:
            logging.info(
                "Message delivered to {} [{}]".format(msg.topic(), msg.partition())
            )

    def process(self, element):  # type: ignore
        """Process transform."""
        try:
            self._producer.produce(
                self.attributes["topic"],
                key=element[0].encode("utf-8"),
                value=json.dumps(element[1]),
                callback=self._delivery_report,
            )
            yield element
        except Exception:
            raise KafkaProducerException(topic=self.attributes["topic"])
