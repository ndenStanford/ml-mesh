# Standard Library
import os

# 3rd party libraries
import pytest
from neptune.attributes.atoms.file import File

# Internal libraries
from onclusiveml.ml_tracking.download import (
    _convert_neptune_data_path_to_local_path,
    _derive_and_filter_file_neptune_data_paths,
    _extract_file_attributes,
)


def extract_file_attributes_test(
    test_uploaded_attributes, test_extracted_file_attributes_expected
):

    test_extracted_file_attributes_actual = _extract_file_attributes(
        test_uploaded_attributes
    )
    # access ._path attributes to enable comparisons
    actual = set(
        ["|".join(item._path) for item in test_extracted_file_attributes_actual]
    )
    expected = set(
        ["|".join(item._path) for item in test_extracted_file_attributes_expected]
    )
    assert actual == expected


@pytest.mark.parametrize("neptune_reference_prefix", ["c", ""])
def derive_and_filter_file_neptune_data_paths_test(
    test_extracted_file_attributes_expected,
    neptune_reference_prefix,
    test_extension,
    monkeypatch,
    test_derive_and_filter_file_neptune_data_paths_expected,
):
    # mock up the `fetch_extension` method
    def mock_fetch_extension(self):

        return test_extension

    monkeypatch.setattr(File, "fetch_extension", mock_fetch_extension)

    test_derive_and_filter_file_neptune_data_paths_actual = (
        _derive_and_filter_file_neptune_data_paths(
            test_extracted_file_attributes_expected,
            neptune_reference_prefix=neptune_reference_prefix,
        )
    )

    assert set(test_derive_and_filter_file_neptune_data_paths_actual) == set(
        test_derive_and_filter_file_neptune_data_paths_expected
    )


@pytest.mark.parametrize(
    "neptune_data_path,neptune_reference_prefix,local_directory_path,local_path_expected",
    [
        ("a/b/c", "a/b", ".", os.path.join(".", "c")),
        ("a/b/c", "", ".", os.path.join(".", "a", "b", "c")),
        ("e/f/g/h", "e", "./subdir", os.path.join("./subdir", "f", "g", "h")),
        ("e/f/g/h", "e/f", "./subdir", os.path.join("./subdir", "g", "h")),
        ("e/f/g/h", "e/f", ".", os.path.join(".", "g", "h")),
    ],
)
def convert_neptune_data_path_to_local_path_test(
    neptune_data_path,
    neptune_reference_prefix,
    local_directory_path,
    local_path_expected,
):

    local_path_actual = _convert_neptune_data_path_to_local_path(
        neptune_data_path=neptune_data_path,
        neptune_reference_prefix=neptune_reference_prefix,
        local_directory_path=local_directory_path,
    )

    assert local_path_actual == local_path_expected
