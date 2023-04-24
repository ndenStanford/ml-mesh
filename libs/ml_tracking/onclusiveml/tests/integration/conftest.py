# Standard Library
import os

# 3rd party libraries
import pytest
from neptune import ModelVersion


@pytest.fixture()
def test_file_directory_upload():

    return "./libs/ml_tracking/onclusiveml/tests/integration/test_file_directory"


@pytest.fixture()
def test_file_directory_download(test_file_directory_upload):

    path = f"{test_file_directory_upload}_download"

    if not os.path.isdir(path):
        os.makedirs(path)

    return path


@pytest.fixture
def test_model_version():

    return ModelVersion(
        model="TES-TEST",
        with_id="TES-TEST-35",
        project="onclusive/test",
        api_token=os.environ.get("NEPTUNE_API_TOKEN"),  # your credentials
    )


@pytest.fixture
def test_config():

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
