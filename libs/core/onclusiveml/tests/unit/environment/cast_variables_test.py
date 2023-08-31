"""Conversion tests."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.environment.cast_variables import (
    as_boolean,
    as_float,
    as_integer,
)


@pytest.mark.parametrize(
    "env_var_value,expected_bool",
    [
        ("true", True),
        ("t", True),
        ("yes", True),
        ("y", True),
        (" TrUe ", True),
        (" T ", True),
        (" YeS ", True),
        (" Y ", True),
        ("false", False),
        ("f", False),
        ("", False),
        ("no", False),
        ("n", False),
        (" FaLsE ", False),
        (" F ", False),
        (" NO ", False),
        (" N ", False),
    ],
)
def as_boolean_test(env_var_value, expected_bool):
    """Boolean conversion test."""
    assert as_boolean(env_var_value) == expected_bool


def as_boolean_raise_value_error_test():
    """Boolean conversion with error."""
    with pytest.raises(ValueError):
        as_boolean("not a boolean value")


@pytest.mark.parametrize(
    "env_var_value,expected_float",
    [
        (" 1.0 ", 1.0),
        (" 0.3124 ", 0.3124),
        (" 1.31e-2 ", 1.31e-2),
        (" 10.1e2 ", 10.1e2),
    ],
)
def as_float_test(env_var_value, expected_float):
    """Float conversion."""
    assert as_float(env_var_value) == expected_float


@pytest.mark.parametrize(
    "invalid_env_var_value,", ["invalid value", " True ", " -10-e1"]
)
def as_float_raise_value_error_test(invalid_env_var_value):
    """Float conversion with error."""
    with pytest.raises(ValueError):
        as_float(invalid_env_var_value)


@pytest.mark.parametrize(
    "env_var_value,expected_integer",
    [
        (" -1 ", -1),
        (" 1 ", 1),
        (" 100 ", 100),
        (" -100 ", -100),
    ],
)
def as_integer_test(env_var_value, expected_integer):
    """Integer conversion test."""
    assert as_integer(env_var_value) == expected_integer


@pytest.mark.parametrize(
    "invalid_env_var_value,", ["invalid value", "1.0", "0.4", "5e2", "5e-2"]
)
def as_integer_raise_value_error_test(invalid_env_var_value):
    """Integer conversion with error."""
    with pytest.raises(ValueError):
        as_integer(invalid_env_var_value)
