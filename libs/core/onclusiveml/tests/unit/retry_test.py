"""Retry."""

# Standard Library
import time
from unittest.mock import patch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.retry import retry


@pytest.mark.parametrize(
    "tries, delay, backoff",
    [(3, 1, 2), (10, 0, 1)],
)
@patch.object(time, "sleep")
def test_retry(mock_sleep, tries, delay, backoff):
    """Test retry with delay and backoff"""

    hit = [0]

    @retry(tries=tries, delay=delay, backoff=backoff)
    def f():
        hit[0] += 1
        1 / 0

    with pytest.raises(ZeroDivisionError):
        f()

    assert hit[0] == tries
    assert mock_sleep.call_count == tries - 1


@pytest.mark.parametrize(
    "return_value",
    [1, 10],
)
def test_tries_inf(return_value):
    """Test infinite retries."""
    hit = [0]

    @retry(tries=float("inf"))
    def f():
        hit[0] += 1
        if hit[0] == return_value:
            return return_value
        else:
            raise ValueError

    assert f() == return_value


@pytest.mark.parametrize(
    "tries, delay, backoff",
    [(1, 0, 0), (10, 0, 1)],
)
@patch.object(time, "sleep")
def test_max_delay(mock_sleep, tries, delay, backoff):
    hit = [0]

    @retry(tries=tries, delay=delay, max_delay=delay, backoff=backoff)
    def f():
        hit[0] += 1
        1 / 0

    with pytest.raises(ZeroDivisionError):
        f()
    assert hit[0] == tries
    assert mock_sleep.call_count == tries - 1


@pytest.mark.parametrize(
    "tries, jitter",
    [(12, 1), (2, 4)],
)
@patch.object(time, "sleep")
def test_fixed_jitter(mock_sleep, tries, jitter):
    """Test retry with jitter."""

    hit = [0]

    @retry(tries=tries, jitter=jitter)
    def f():
        hit[0] += 1
        1 / 0

    with pytest.raises(ZeroDivisionError):
        f()

    assert hit[0] == tries
    assert mock_sleep.call_count == tries - 1
