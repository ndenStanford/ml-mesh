"""Artifacts."""

# Standard Library
import json
import os

# Internal libraries
from onclusiveml.core.base.pydantic import OnclusiveBaseSettings


class ServedModelArtifacts(object):
    """Served model artifacts."""

    def __init__(
        self, settings: OnclusiveBaseSettings, remove_model_prefix: bool = True
    ):
        """Utility class that reads in the model card and assembles model artifact local paths.

        Note:
            Assumes that the neptune file attribute paths have been mapped to relative local paths
            (e.g. as the `TrackedModelVersion.download_directory_from_model_version` method does)
        """
        self.model_name = settings.model_name
        self.model_directory = settings.model_directory
        # load model card
        if remove_model_prefix:
            self.model_card_file = os.path.join(self.model_directory, "model_card")
        else:
            self.model_card_file = os.path.join(
                self.model_directory, "models", "model_card"
            )

        json_file = open(self.model_card_file)
        self.model_card = json.load(json_file)
        json_file.close()
        # obtain directory for model artifacts from model card
        self.model_artifact_directory = os.path.join(
            self.model_directory, self.model_card["model_artifact_attribute_path"]
        )
        # obtain file paths for test files from model card
        self.inputs_test_file = os.path.join(
            self.model_directory, self.model_card["model_test_files"]["inputs"]
        )

        self.inference_params_test_file = os.path.join(
            self.model_directory,
            self.model_card["model_test_files"]["inference_params"],
        )

        self.predictions_test_file = os.path.join(
            self.model_directory, self.model_card["model_test_files"]["predictions"]
        )

        if remove_model_prefix:
            model_prefix_pattern = "model" + os.sep
            self.inputs_test_file = self.inputs_test_file.replace(
                model_prefix_pattern, ""
            )
            self.inference_params_test_file = self.inference_params_test_file.replace(
                model_prefix_pattern, ""
            )
            self.predictions_test_file = self.predictions_test_file.replace(
                model_prefix_pattern, ""
            )
            self.model_artifact_directory = self.model_artifact_directory.replace(
                model_prefix_pattern, ""
            )
