# Standard Library
from typing import Any, List

# 3rd party libraries
import pytest
from neptune.attributes.atoms.file import File


def test_file(path: List[Any]):
    return File(container=[], path=path)


@pytest.fixture
def test_uploaded_attributes():

    return {
        "a": 1,
        "b": test_file(["b"]),
        "c": {
            "d": {"e": test_file(path=["c", "d", "e"]), "f": 2},
            "g": test_file(path=["c", "g"]),
        },
    }


@pytest.fixture
def test_extracted_file_attributes_expected():

    return [test_file(["b"]), test_file(["c", "d", "e"]), test_file(["c", "g"])]


@pytest.fixture
def test_derive_and_filter_neptune_attribute_paths_expected(neptune_attribute_prefix):

    result = ["c/d/e", "c/g"]

    if neptune_attribute_prefix == "c":
        return result
    elif neptune_attribute_prefix == "":
        result.insert(0, "b")
        return result
    else:
        raise ValueError('Only values "c" and "" are suppported by this fixture.')
