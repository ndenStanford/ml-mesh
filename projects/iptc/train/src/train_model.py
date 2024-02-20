"""Register trained model."""

# Standard Library
import os
from typing import Dict, List, Union

# ML libs
from transformers import pipeline

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelVersion


logger = get_default_logger(__name__)

# Source
from src.settings import (  # type: ignore[attr-defined]
    CLASS_DICT,
    ID_TO_TOPIC,
    MODEL_ID,
    BaseTrackedModelSpecs,
    TrackedIPTCBaseModelCard,
    TrackedIPTCModelSpecs,
)


# def upload_single_model(model_path):
def main() -> None:
    """Download and Register main method."""
    # get read-only base model version
    base_model_specs = BaseTrackedModelSpecs()
    logger.info(msg=str(base_model_specs.dict()))
    base_model_version = TrackedModelVersion(**base_model_specs.dict())
    # get base model version assets to local disk
    base_model_card: Dict = base_model_version.download_config_from_model_version(
        neptune_attribute_path="model/model_card"
    )

    model_specs = TrackedIPTCModelSpecs()
    model_card = TrackedIPTCBaseModelCard()
    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # download model artifact
    base_model_version.download_directory_from_model_version(
        local_directory_path=model_card.local_output_dir,
        neptune_attribute_path=base_model_card["model_artifact_attribute_path"],
    )

    logger.info(
        f"Successfully downloaded base iptc model into "
        f"{model_card.local_output_dir}"
    )

    base_model_version.stop()
    # initialize registered model on neptune ai
    model_version = TrackedModelVersion(**model_specs.dict())
    # Create pipeline using base model on neptune
    logger.info("Create pipeline using base model on neptune")
    base_model_pipeline = pipeline(
        task=base_model_card["model_params"]["huggingface_pipeline_task"],
        model=model_card.local_output_dir,
    )
    # iptc settings
    iptc_settings = model_card.model_params.iptc_settings.dict()
    # --- create prediction files
    logger.info("Making predictions from example inputs")
    iptc_predictions: List[Dict[str, Union[str, float, int]]] = base_model_pipeline(
        model_card.model_inputs.sample_documents
    )
    # Convert score's value from np.float32 to just float
    # Reason for this is because float32 types are not JSON serializable

    for dictionary in iptc_predictions:
        dictionary["score"] = float(dictionary["score"])
        dictionary["label"] = CLASS_DICT[ID_TO_TOPIC[MODEL_ID]][dictionary["label"]]
    # --- add assets to registered model version on neptune ai
    # testing assets - inputs, inference specs and outputs
    logger.info("Pushing assets to neptune AI")
    for (test_file, test_file_attribute_path) in [
        (model_card.model_inputs.sample_documents, model_card.model_test_files.inputs),
        (iptc_settings, model_card.model_test_files.inference_params),
        (iptc_predictions, model_card.model_test_files.predictions),
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
