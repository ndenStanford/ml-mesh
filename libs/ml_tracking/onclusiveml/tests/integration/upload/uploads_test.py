# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.ml_tracking.upload import (
    capture_directory_for_upload,
    upload_config_to_model_version,
    upload_directory_to_model_version,
    upload_file_to_model_version,
)


@pytest.mark.upload
@pytest.mark.parametrize(
    "file_name,file_extension",
    [
        ("test_file_1", "json"),
        ("test_file_2", "txt"),
    ],
)
def upload_file_to_model_version_test(
    test_model_version, test_file_directory_upload, file_name, file_extension
):

    upload_file_to_model_version(
        model_version=test_model_version,
        local_file_path=f"{test_file_directory_upload}/{file_name}.{file_extension}",
        neptune_attribute_path=f"model/{file_name}",
    )

    test_model_version.stop()


@pytest.mark.upload
@pytest.mark.parametrize(
    "neptune_attribute_path", ["", "some_attribute_path", "some/nested/attribute/path"]
)
@pytest.mark.parametrize("exclude", [[], [".", "__"]])
def capture_directory_for_upload_test(
    test_file_directory_upload,
    exclude,
    neptune_attribute_path,
    test_captured_directories_for_upload_expected,
):

    test_captured_directories_for_upload_actual = capture_directory_for_upload(
        local_directory_path=test_file_directory_upload,
        neptune_attribute_path=neptune_attribute_path,
        exclude=exclude,
    )

    assert set(test_captured_directories_for_upload_actual) == set(
        test_captured_directories_for_upload_expected
    )


@pytest.mark.upload
def upload_directory_to_model_version_test(
    test_model_version, test_file_directory_upload
):

    upload_directory_to_model_version(
        model_version=test_model_version,
        local_directory_path=test_file_directory_upload,
        neptune_attribute_path="model/test_file_directory",
    )

    test_model_version.stop()


@pytest.mark.upload
def upload_config_to_model_version_test(test_model_version, test_config_expected):

    upload_config_to_model_version(
        model_version=test_model_version,
        config=test_config_expected,
        neptune_attribute_path="test_config",
    )

    test_model_version.stop()
