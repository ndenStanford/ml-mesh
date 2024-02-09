"""Baseclass for optimizing Onclusive models. Inherited by training and compiling modules."""

# Standard Library
from typing import List

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedModelVersion,
)


class OnclusiveModelOptimizer:
    """Class for training and managing Onclusive models."""

    def __init__(
        self,
        tracked_model_specs: TrackedModelSpecs,
        model_card: TrackedModelCard,
    ) -> None:
        """Initialize the OnclusiveModelTrainer.

        Args:
            tracked_model_specs (TrackedModelSpecs): Specifications for tracked model on neptune.
            model_card (TrackedModelCard): Model card with specifications of the model.

        Returns: None
        """
        self.tracked_model_specs = tracked_model_specs
        self.model_card = model_card
        self.create_tracked_model_version()

        self.logger = get_default_logger(__name__)

    def create_tracked_model_version(self) -> None:
        """Create tracked model version object for optimizer class.

        Returns: None
        """
        self.tracked_model_version = TrackedModelVersion(
            **self.tracked_model_specs.dict()
        )

    def upload_model_to_neptune(
        self,
        test_files: List,
        test_file_attribute_paths: List,
        model_local_directory: str,
    ) -> None:
        """Upload model-related information to Neptune.

        Args:
            test_files (List): List of test files.
            test_file_attribute_paths (List): List of attribute paths for test files.
            model_local_directory (str): Local directory path with the saved model.

        Returns: None
        """
        for (test_file, test_file_attribute_path) in zip(
            test_files, test_file_attribute_paths
        ):
            self.tracked_model_version.upload_config_to_model_version(
                config=test_file, neptune_attribute_path=test_file_attribute_path
            )

        self.tracked_model_version.upload_directory_to_model_version(
            local_directory_path=model_local_directory,
            neptune_attribute_path=self.model_card.model_artifact_attribute_path,
        )
        # # model card
        self.tracked_model_version.upload_config_to_model_version(
            config=self.model_card.dict(), neptune_attribute_path="model/model_card"
        )
        self.tracked_model_version.stop()

    def __call__(
        self,
        test_files: List,
        test_file_attribute_paths: List,
        model_local_directory: str,
    ) -> None:
        """Call Method."""
        self.upload_model_to_neptune(
            test_files, test_file_attribute_paths, model_local_directory
        )
