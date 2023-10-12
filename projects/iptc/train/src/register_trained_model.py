"""Register trained model."""

# Standard Library
import os
import pickle
from typing import Dict, List, Union

# ML libs
import torch
from transformers import pipeline

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelVersion


logger = get_default_logger(__name__)

# Source
from src.settings import (  # type: ignore[attr-defined]
    CLASS_DICT_FIRST,
    TrackedIPTCBaseModelCard,
    TrackedIPTCModelSpecs,
)


# def upload_single_model(model_path):
def main() -> None:
    """Register main method."""
    model_specs = TrackedIPTCModelSpecs()
    model_card = TrackedIPTCBaseModelCard()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # initialize registered model on neptune ai
    model_version = TrackedModelVersion(**model_specs.dict())
    # --- initialize models
    # get pretrained model and tokenizer
    logger.info("Initializing model and tokenizer")
    model = torch.load("/projects/iptc/train/models/model.pt")
    tokenizer = pickle.load(open("/projects/iptc/train/models/tokenizer.vocab", "rb"))
    # Create pipeline using iptc model and tokenizer
    logger.info("Creating huggingface pipeline")
    hf_pipeline = pipeline(
        task=model_card.model_params.huggingface_pipeline_task,
        model=model,
        tokenizer=tokenizer,
    )
    # iptc settings
    iptc_settings = model_card.model_params.iptc_settings.dict()
    # --- create prediction files
    logger.info("Making predictions from example inputs")
    iptc_predictions: List[Dict[str, Union[str, float, int]]] = hf_pipeline(
        model_card.model_inputs.sample_documents
    )
    # Convert score's value from np.float32 to just float
    # Reason for this is because float32 types are not JSON serializable
    for dictionary in iptc_predictions:
        dictionary["score"] = float(dictionary["score"])
        dictionary["label"] = CLASS_DICT_FIRST["root"][dictionary["label"]]
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
    hf_pipeline_local_dir = os.path.join(model_card.local_output_dir, "hf_pipeline")
    # hf_pipeline.save_pretrained(hf_pipeline_local_dir)
    model.save_pretrained(hf_pipeline_local_dir)
    tokenizer.vocab_file = "/projects/iptc/train/models/tokenizer.vocab"

    tokenizer.save_vocabulary(hf_pipeline_local_dir)

    model_version.upload_directory_to_model_version(
        local_directory_path=hf_pipeline_local_dir,
        neptune_attribute_path=model_card.model_artifact_attribute_path,
    )
    # model card
    model_version.upload_config_to_model_version(
        config=model_card.dict(), neptune_attribute_path="model/model_card"
    )

    model_version.stop()


if __name__ == "__main__":
    main()
