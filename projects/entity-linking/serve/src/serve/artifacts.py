"""Settings."""

# Standard Library
import json
import os

# Internal libraries
from onclusiveml.core.base.pydantic import OnclusiveBaseSettings


class BelaModelArtifacts(object):
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

        self.model_artifact_directory = os.path.join(
            self.model_directory, "model_artifacts"
        )

        # obtain directory for model from model card
        self.model_model_directory = os.path.join(
            self.model_artifact_directory, "model_wiki.ckpt"
        )
        # obtain directory for embedding from model card
        self.model_embeddings_directory = os.path.join(
            self.model_artifact_directory,
            self.model_card["model_params"]["embeddings_filename"],
        )
        # obtain directory for index from model card
        self.model_index_directory = os.path.join(
            self.model_artifact_directory,
            self.model_card["model_params"]["index_filename"],
        )
