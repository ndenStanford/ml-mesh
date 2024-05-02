"""Register trained model."""

# Standard Library
import os

# 3rd party libraries
from huggingface_hub import hf_hub_download

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelVersion


logger = get_default_logger(__name__)

# Source
from src.settings import (  # type: ignore[attr-defined]
    TrackedEntityLinkingBaseModelCard,
    TrackedEntityLinkingModelSpecs,
)


def main() -> None:
    """Register main method."""
    model_specs = TrackedEntityLinkingModelSpecs()
    model_card = TrackedEntityLinkingBaseModelCard()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # initialize registered model on neptune ai
    model_version = TrackedModelVersion(**model_specs.dict())

    checkpoint_name_path = f"model_{model_card.model_params.checkpoint_name}.ckpt"
    hf_hub_download(
        repo_id=model_card.model_params.repo,
        filename=model_card.model_params.embeddings_filename,
        local_dir=model_card.local_output_dir,
    )
    hf_hub_download(
        repo_id=model_card.model_params.repo,
        filename=model_card.model_params.index_filename,
        local_dir=model_card.local_output_dir,
    )
    hf_hub_download(
        repo_id=model_card.model_params.repo,
        filename=checkpoint_name_path,
        local_dir=model_card.local_output_dir,
    )

    entity_linking_settings = model_card.model_params.entity_linking_settings.dict()

    logger.info("Pushing assets to neptune AI")
    for (test_file, test_file_attribute_path) in [
        (entity_linking_settings, model_card.model_test_files.inference_params),
    ]:
        model_version.upload_config_to_model_version(
            config=test_file, neptune_attribute_path=test_file_attribute_path
        )
    logger.info("Pushing model artifact and assets to s3")
    # model artifact
    model_version.upload_directory_to_model_version(
        local_directory_path=model_card.local_output_dir,
        neptune_attribute_path=model_card.model_artifact_attribute_path,
    )
    # model card
    model_version.upload_config_to_model_version(
        config=model_card.dict(), neptune_attribute_path="model/model_card"
    )

    model_version.stop()


if __name__ == "__main__":
    main()
