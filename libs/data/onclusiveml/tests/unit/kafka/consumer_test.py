"""Consumer test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.data.kafka import OnclusiveKakfaConsumer


def test_consumer_init_fail():
    """Test failed initialization."""
    with pytest.raises(ValueError):
        _ = OnclusiveKakfaConsumer({}, topics=[])


def test_consumer_init():
    """Test failed initialization."""
    _ = OnclusiveKakfaConsumer({"group.id": ""}, topics=[])


def test_consumer_poll():
    """Test consumer poll."""
    consumer = OnclusiveKakfaConsumer(
        {"group.id": "dummygroup"}, topics=["test.topic"], test=True
    )
    msg = consumer.poll(timeout=0.001)
    assert msg is None


def test_consumer_iteration():
    """Test consumer poll."""
    consumer = OnclusiveKakfaConsumer(
        {"group.id": "dummygroup"}, topics=["test.topic"], test=True
    )
    assert len(list(consumer)) == 0
