"""Retry."""

# Standard Library
import functools
import logging
import random
import time
from typing import Any, Callable, Optional, Tuple, Union

# Internal libraries
from onclusiveml.core.decorator import decorator
from onclusiveml.core.logging import INFO, get_default_logger


logger = get_default_logger(name=__name__, level=INFO)


def _retry(
    f: Callable,
    exception: type = Exception,
    tries: int = -1,
    delay: float = 0,
    max_delay: Optional[float] = None,
    backoff: float = 1,
    jitter: Union[float, Tuple[float]] = 0,
    logger: logging.Logger = logger,
) -> Any:
    """Calls a method and retries if the call raises an exception.

    Args:

        f: the method to execute.
        exception: an exception or a tuple of exceptions to catch. default: Exception.
        tries: the maximum number of attempts. default: 1 (1 retry).
        delay: initial delay between attempts. default: 0.
        max_delay: the maximum value of delay. default: None (no limit).
        backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
        jitter: extra seconds added to delay between attempts. default: 0.
                    fixed if a number, random if a range tuple (min, max)
        logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                    default: retry.logger. if None, logging is disabled.

    Returns:
        the result of the input method f.
    """
    _tries, _delay = tries, delay
    while _tries:
        try:
            return f()
        except exception as e:  # type: ignore[misc]
            _tries -= 1
            if not _tries:
                raise

            if logger is not None:
                logger.warning("%s, retrying in %s seconds...", e, _delay)

            time.sleep(_delay)

            _delay *= backoff

            if isinstance(jitter, tuple):
                _delay += random.uniform(*jitter)  # type: ignore[call-arg]
            else:
                _delay += jitter

            if max_delay is not None:
                _delay = min(_delay, max_delay)


def retry(
    exception: type = Exception,
    tries: int = -1,
    delay: float = 0,
    max_delay: Optional[float] = None,
    backoff: float = 1,
    jitter: Union[float, Tuple[float]] = 0,
    logger: logging.Logger = logger,
) -> Any:
    """Returns a retry decorator.

    Args:

        f: the method to execute.
        exception: an exception or a tuple of exceptions to catch. default: Exception.
        tries: the maximum number of attempts. default: 1 (1 retry).
        delay: initial delay between attempts. default: 0.
        max_delay: the maximum value of delay. default: None (no limit).
        backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
        jitter: extra seconds added to delay between attempts. default: 0.
                    fixed if a number, random if a range tuple (min, max)
        logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                    default: retry.logger. if None, logging is disabled.

    Returns:
        a retry decorator.
    """

    @decorator
    def retry_decorator(f: Callable, *fargs: Any, **fkwargs: Any) -> Callable:
        args = fargs if fargs else list()
        kwargs = fkwargs if fkwargs else dict()
        return _retry(
            functools.partial(f, *args, **kwargs),
            exception,
            tries,
            delay,
            max_delay,
            backoff,
            jitter,
            logger,
        )

    return retry_decorator
