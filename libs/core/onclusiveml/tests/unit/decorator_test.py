"""Test decorator."""

# Standard Library
from typing import Any, Callable

# Internal libraries
from onclusiveml.core.decorator import decorator


@decorator
def print_decorator(f: Callable, *fargs: Any) -> Callable:
    args = fargs if fargs else list()

    def g(*args):
        return f(*args)

    return args, g(*args)


def test_decorator():
    """Test that decorator returns decorated result."""

    def f(x):
        return x

    h = print_decorator(f)

    assert (2,), f(2) == h(2)  # noqa: F631
