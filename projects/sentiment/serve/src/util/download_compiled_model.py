"""Download compiled model."""

# Standard Library
import os

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.util.params import ServedModelParams, TrackedCompiledModelSpecs


if __name__ == "__main__":
    """Download compiled model."""
    logger = get_default_logger(__name__)
    # model registry reference to the desired (compiled) model version
    model_version_specs = TrackedCompiledModelSpecs()
    # output directory specs
    model_export_params = ServedModelParams()
    # initialize client for specific model version
    mv = TrackedModelVersion(**model_version_specs.dict())

    if not os.path.isdir(model_export_params.model_directory):
        # if the target dir does not exist, download all model artifacts for the model version to
        # local
        print(
            "model_export_params.model_directory: ", model_export_params.model_directory
        )
        mv.download_directory_from_model_version(
            local_directory_path=model_export_params.model_directory,
            neptune_attribute_path="model",
        )
    elif not os.listdir(model_export_params.model_directory):
        # if the target dir does exist but is empty, download all model artifacts for the model
        # version to local
        mv.download_directory_from_model_version(
            local_directory_path=model_export_params.model_directory,
            neptune_attribute_path="model",
        )
    else:
        logger.info(
            f"The specified output directory {model_export_params.model_directory} already "
            f"exists and is not empty: {os.listdir(model_export_params.model_directory)}. Model "
            "download skipped."
        )
    # shutdown client
    mv.stop()
