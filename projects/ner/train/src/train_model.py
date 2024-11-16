"""Register trained model."""

# Standard Library
import os
from typing import Dict, List, Union

# ML libs
from transformers import (  # noqa
    AutoModelForTokenClassification,
    AutoTokenizer,
    pipeline,
)

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import get_settings


logger = get_default_logger(__name__)
settings = get_settings()


def main() -> None:
    """Register trained model."""
    model_specs = settings.model_specs
    model_card = settings.model_card

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # initialize registered model on neptune ai
    model_version = TrackedModelVersion(**model_specs.model_dump())
    # --- initialize models
    # get pretrained model and tokenizer
    # Create pipeline using ner model and tokenizer
    logger.info("Creating NER pipeline")
    model_class = eval(model_card.ner_model_params_base.model_class)
    tokenizer_class = eval(model_card.ner_model_params_base.tokenizer_class)
    model_base = model_class.from_pretrained(
        model_card.ner_model_params_base.huggingface_model_reference, return_dict=False
    )
    tokenizer_base = tokenizer_class.from_pretrained(
        model_card.ner_model_params_base.huggingface_model_reference
    )

    hf_pipeline = pipeline(
        task=model_card.ner_model_params_base.huggingface_pipeline_task,
        model=model_base,
        tokenizer=tokenizer_base,
    )
    # # Create pipeline using ner model and tokenizer
    # ner settings
    ner_settings = model_card.ner_model_params_base.ner_settings.dict()
    # --- create prediction files
    logger.info("Making predictions from example inputs")
    ner_predictions: List[List[Dict[str, Union[str, float, int]]]] = hf_pipeline(
        model_card.model_inputs.sample_documents[0]
    )
    # Convert score's value from np.float32 to just float
    # Reason for this is because float32 types are not JSON serializable
    for sublist in ner_predictions:
        for dictionary in sublist:
            dictionary["score"] = float(dictionary["score"])
    # --- add assets to registered model version on neptune ai
    # testing assets - inputs, inference specs and outputs
    logger.info("Pushing assets to neptune AI")
    for test_file, test_file_attribute_path in [
        (
            model_card.model_inputs.sample_documents,
            model_card.model_test_files.inputs,
        ),
        (
            ner_settings,
            model_card.model_test_files.inference_params,
        ),
        (
            ner_predictions,
            model_card.model_test_files.predictions,
        ),
    ]:
        model_version.upload_config_to_model_version(
            config=test_file, neptune_attribute_path=test_file_attribute_path
        )

    logger.info("Pushing model artifact and assets to s3")
    # model artifact for original
    hf_pipeline_local_dir = os.path.join(
        model_card.local_output_dir, "hf_pipeline_base"
    )
    hf_pipeline.save_pretrained(hf_pipeline_local_dir)

    model_version.upload_directory_to_model_version(
        local_directory_path=hf_pipeline_local_dir,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.base_model_subdirectory,
    )
    # model card
    model_version.upload_config_to_model_version(
        config=model_card.model_dump(), neptune_attribute_path="model/model_card"
    )

    model_version.stop()


if __name__ == "__main__":
    main()
