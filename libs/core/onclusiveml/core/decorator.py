"""Decorator."""

# Standard Library
import functools
from typing import Any, Callable


def decorator(caller: Callable) -> Callable:
    """Turns caller into a decorator.

    Unlike decorator module, function signature is not preserved.

    Args:
        caller: Callable
    """

    def decor(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return caller(f, *args, **kwargs)

        return wrapper

    return decor
