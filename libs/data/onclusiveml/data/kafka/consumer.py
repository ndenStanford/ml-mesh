"""Kafka internal object."""

# Standard Library
import logging
from typing import Any, Dict, List, Tuple

# 3rd party libraries
from confluent_kafka import Consumer, KafkaError, TopicPartition


class OnclusiveKakfaConsumer(Consumer):
    """Onclusive Kakfa consumer."""

    def __init__(
        self, config: Dict, topics: List[str], timeout: float = 0.01, test: bool = False
    ):
        if test:
            config.update({"on_commit": self.test_commit_callback})
        Consumer.__init__(self, config)
        if topics:
            self.subscribe(topics)
        self.timeout = timeout

    def test_commit_callback(err: KafkaError, partitions: TopicPartition) -> Any:
        """Dummy commit callback for testing purposes."""

    def __iter__(self) -> "OnclusiveKakfaConsumer":
        return self

    def __next__(self) -> Tuple[str, str]:
        try:
            msg = self.poll(self.timeout)
            return msg.key().decode("utf-8"), msg.value().decode("utf-8")
        except Exception as e:
            logging.debug(e)
            raise StopIteration
