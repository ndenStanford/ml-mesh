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
def test_extension():

    return "test_ext"


@pytest.fixture
def test_derive_and_filter_file_neptune_data_paths_expected(
    neptune_reference_prefix, test_extension
):

    result = [("c/d/e", f"c/d/e.{test_extension}"), ("c/g", f"c/g.{test_extension}")]

    if neptune_reference_prefix == "c":
        return result
    elif neptune_reference_prefix == "":
        result.insert(0, ("b", f"b.{test_extension}"))
        return result
    else:
        raise ValueError('Only values "c" and "" are suppported by this fixture.')
