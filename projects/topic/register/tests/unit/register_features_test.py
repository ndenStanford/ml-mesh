"""Test resgister features script."""

# Standard Library
from unittest.mock import Mock, call

# 3rd party libraries
import pytest

# Source
from src.register_features import (
    FeastRepoBuilder,
    plan_repo_contents,
    register_repo_contents,
)


@pytest.fixture
def feast_repo_builder_mock():
    """Creates a mock FeastRepoBuilder object.

    This function returns a mock object that is a subclass of FeastRepoBuilder.
    It is useful for creating test instances where you want to replace the actual
    FeastRepoBuilder with a mock.

    Args:
        None

    Returns:
        Mock: A mock object with the same specifications as FeastRepoBuilder.

    """
    return Mock(spec=FeastRepoBuilder)


def test_register_repo_contents(feast_repo_builder_mock):
    """Unit test for the register_repo_contents function.

    This test case uses a mocked FeastRepoBuilder to ensure that the register_repo_contents
    function correctly registers entities and features and logs the expected information.

    Args:
        feast_repo_builder_mock (Mock): A mocked FeastRepoBuilder object.

    Returns:
        None

    """
    # Mocking necessary dependencies
    feast_repo_builder_mock.entity = Mock()
    feast_repo_builder_mock.feature_view = Mock()
    feast_repo_builder_mock.fs_handle = Mock()
    feast_repo_builder_mock.fs_handle.list_entities.return_value = [Mock(name="entity")]
    feast_repo_builder_mock.fs_handle.list_data_sources.return_value = [
        Mock(name="data_scource")
    ]
    feast_repo_builder_mock.fs_handle.list_feature_views.return_value = [
        Mock(name="feature_view")
    ]
    # Call the function
    register_repo_contents(feast_repo_builder_mock)
    # Assert that register is called with the expected arguments
    feast_repo_builder_mock.fs_handle.register.assert_has_calls(
        [
            call([feast_repo_builder_mock.entity]),
            call([feast_repo_builder_mock.feature_view]),
        ]
    )


class MockStringWithToString(str):
    """A custom string class with a custom to_string method.

    This class is a subclass of the built-in str class and adds a custom method
    `to_string` which returns the string representation of the object.

    Attributes:
        None

    Methods:
        to_string(): Returns the string representation of the object.

    """

    def to_string(self):
        """Returns the string representation of the object."""
        return str(self)


def test_plan_repo_contents(feast_repo_builder_mock):
    """Unit test for the plan_repo_contents function.

    This test case uses a mocked FeastRepoBuilder to ensure that the plan_repo_contents
    function correctly generates a plan for registering feast components and logs the
    expected differences.

    Args:
        feast_repo_builder_mock (Mock): A mocked FeastRepoBuilder object.

    Returns:
        None

    """
    # Mocking necessary dependencies
    feast_repo_builder_mock.data_source = Mock()
    feast_repo_builder_mock.entity = Mock()
    feast_repo_builder_mock.feature_view = Mock()
    feast_repo_builder_mock.fs_handle = Mock()
    registry_diff_mock = MockStringWithToString("registry_diff")
    feast_repo_builder_mock.fs_handle.plan.return_value = (
        registry_diff_mock,
        "infra_diff",
        "new_infra",
    )
    # Call the function
    plan_repo_contents(feast_repo_builder_mock)
    # Assert that plan is called with the expected arguments
    feast_repo_builder_mock.fs_handle.plan.assert_called_once_with(
        [feast_repo_builder_mock.data_source],
        [feast_repo_builder_mock.feature_view],
        [feast_repo_builder_mock.entity],
    )
