# Internal libraries
from onclusiveml.core.base import OnclusiveEnum


class TestEnum(OnclusiveEnum):

    TEST_1: int = 1
    TEST_2: str = "two"


def test_onclusive_enum():

    assert TestEnum.TEST_1.value == 1
    assert TestEnum.TEST_2.value == "two"

    assert TestEnum.list() == [1, "two"]
