"""Download helpers tests."""

# Standard Library
import os

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.tracking.tracked_model_version import TrackedModelVersion


def test__extract_data_attributes(
    test_uploaded_attributes, test_extracted_data_attributes_expected
):
    """Extract data attributes."""
    test_extracted_data_attributes_actual = (
        TrackedModelVersion._extract_data_attributes(test_uploaded_attributes)
    )
    # access ._path attributes to enable comparisons
    actual = set(
        ["|".join(item._path) for item in test_extracted_data_attributes_actual]
    )
    expected = set(
        ["|".join(item._path) for item in test_extracted_data_attributes_expected]
    )
    assert actual == expected


@pytest.mark.parametrize("neptune_attribute_prefix", ["c", ""])
def test_derive_and_filter_neptune_attributes_paths(
    test_extracted_data_attributes_expected,
    neptune_attribute_prefix,
    test_derive_and_filter_neptune_attribute_paths_expected,
):
    """Test derive and filter neptune attribute paths."""
    test_derive_and_filter_neptune_attribute_paths_actual = (
        TrackedModelVersion._derive_and_filter_neptune_attribute_paths(
            test_extracted_data_attributes_expected,
            neptune_attribute_prefix=neptune_attribute_prefix,
        )
    )

    assert set(test_derive_and_filter_neptune_attribute_paths_actual) == set(
        test_derive_and_filter_neptune_attribute_paths_expected
    )


@pytest.mark.parametrize(
    "neptune_attribute_path,neptune_attribute_prefix,local_directory_path,local_path_expected",
    [
        ("a/b/c", "a/b", ".", os.path.join(".", "c")),
        ("a/b/c", "", ".", os.path.join(".", "a", "b", "c")),
        ("e/f/g/h", "e", "./subdir", os.path.join("./subdir", "f", "g", "h")),
        ("e/f/g/h", "e/f", "./subdir", os.path.join("./subdir", "g", "h")),
        ("e/f/g/h", "e/f", ".", os.path.join(".", "g", "h")),
    ],
)
def test_convert_neptune_data_path_to_local_path(
    neptune_attribute_path,
    neptune_attribute_prefix,
    local_directory_path,
    local_path_expected,
):
    """Test convert neptune data path to local path."""
    local_path_actual = (
        TrackedModelVersion._convert_neptune_attribute_path_to_local_path(
            neptune_attribute_path=neptune_attribute_path,
            neptune_attribute_prefix=neptune_attribute_prefix,
            local_directory_path=local_directory_path,
            create_local_subdirs=False,
        )
    )

    assert local_path_actual == local_path_expected
