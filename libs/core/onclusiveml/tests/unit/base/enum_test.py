"""Test base module."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.base import OnclusiveEnum


class TestEnum(OnclusiveEnum):
    """Test enum class."""

    TEST_1: int = 1
    TEST_2: str = "two"


def test_onclusive_enum():
    """Test enum methods."""
    assert TestEnum.TEST_1.value == 1
    assert TestEnum.TEST_2.value == "two"

    assert TestEnum.values() == [1, "two"]


@pytest.mark.parametrize(
    "name, expected",
    [
        ("TEST_1", TestEnum.TEST_1),
        ("TEST_2", TestEnum.TEST_2),
    ],
)
def test_from_name_method(name, expected):
    """Test from_name method."""
    assert TestEnum.from_name(name) == expected
