# Standard Library
import os

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.tracking.tracked_model_utils import TrackedModelCard
from onclusiveml.tracking.tracked_model_version import TrackedModelVersion


# create a new model version every time the integration test suite is run
TEST_MODEL_VERSION_ID = TrackedModelVersion(
    model="TES-TEST",
    project="onclusive/test",
    api_token=os.environ.get("NEPTUNE_API_TOKEN"),  # your credentials
)._sys_id


@pytest.fixture()
def test_file_directory_upload():

    return "./libs/tracking/onclusiveml/tests/integration/test_file_directory"


@pytest.fixture()
def test_file_directory_download(test_file_directory_upload):

    path = f"{test_file_directory_upload}_downloaded"

    if not os.path.isdir(path):
        os.makedirs(path)

    return path


@pytest.fixture
def test_model_version(test_model_version_mode: str = "async"):

    test_model_version = TrackedModelVersion(
        model="TES-TEST",
        with_id=TEST_MODEL_VERSION_ID,
        project="onclusive/test",
        api_token=os.environ.get("NEPTUNE_API_TOKEN"),  # your credentials
        mode=test_model_version_mode,
    )

    return test_model_version


@pytest.fixture
def test_captured_directories_for_upload_expected(
    test_file_directory_upload, exclude, neptune_attribute_path
):

    neptune_attribute_prefix = (
        "" if not neptune_attribute_path else f"{neptune_attribute_path}/"
    )

    result = [
        (
            os.path.join(
                test_file_directory_upload, "test_file_subdirectory", "test_file_3.yaml"
            ),
            f"{neptune_attribute_prefix}test_file_subdirectory/test_file_3.yaml",
        ),
        (
            os.path.join(test_file_directory_upload, "test_file_1.json"),
            f"{neptune_attribute_prefix}test_file_1.json",
        ),
        (
            os.path.join(test_file_directory_upload, "test_file_2.txt"),
            f"{neptune_attribute_prefix}test_file_2.txt",
        ),
    ]

    if exclude == [".", "__"]:
        pass
    elif exclude == []:
        result.append(
            (
                os.path.join(test_file_directory_upload, "__excluded_test_file.txt"),
                f"{neptune_attribute_prefix}__excluded_test_file.txt",
            )
        )
        result.append(
            (
                os.path.join(test_file_directory_upload, ".excluded_test_file.json"),
                f"{neptune_attribute_prefix}.excluded_test_file.json",
            )
        )
        result.append(
            (
                os.path.join(
                    test_file_directory_upload,
                    "test_file_subdirectory",
                    "__excluded_test_file.yaml",
                ),
                f"{neptune_attribute_prefix}test_file_subdirectory/__excluded_test_file.yaml",
            )
        )
        result.append(
            (
                os.path.join(
                    test_file_directory_upload,
                    "test_file_subdirectory",
                    ".excluded_test_file.yaml",
                ),
                f"{neptune_attribute_prefix}test_file_subdirectory/.excluded_test_file.yaml",
            )
        )
        result.append(
            (
                os.path.join(
                    test_file_directory_upload,
                    "__excluded_test_subdirectory",
                    "__excluded_test_file.txt",
                ),
                f"{neptune_attribute_prefix}__excluded_test_subdirectory/__excluded_test_file.txt",
            )
        )
        result.append(
            (
                os.path.join(
                    test_file_directory_upload,
                    ".excluded_test_subdirectory",
                    ".excluded_test_file.json",
                ),
                f"{neptune_attribute_prefix}.excluded_test_subdirectory/.excluded_test_file.json",
            )
        )

    else:
        raise ValueError('Only [] and [".","__"] are supported by integration tests!')

    return result


@pytest.fixture
def test_config_expected():

    return {
        "letter": "a",
        "float": 0.1,
        "int": 1,
        "int_list": [1, 2, 3, 4],
        "float_list": [1, 2, 3, 4],
        "list_list": [
            ["a", "b", "c", "d"],
            [0.1, 0.2, 0.3, 0.4],
            [1, 2, 3, 4],
        ],
    }


@pytest.fixture
def test_model_card_expected():

    return TrackedModelCard(model_type="base").dict()
