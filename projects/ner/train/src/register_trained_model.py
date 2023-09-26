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
    TrackedNERBaseModelCard,
    TrackedNERModelSpecs,
)


def main() -> None:
    """Register trained model."""
    model_specs = TrackedNERModelSpecs()
    model_card = TrackedNERBaseModelCard()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # initialize registered model on neptune ai
    model_version = TrackedModelVersion(**model_specs.dict())
    # --- initialize models
    # get pretrained model and tokenizer

    # Create pipeline using ner model and tokenizer
    logger.info("Creating base NER pipeline")
    hf_pipeline = pipeline(
        task=model_card.ner_model_params_base.huggingface_pipeline_task,
        model=model_card.ner_model_params_base.huggingface_model_reference,
        tokenizer=model_card.ner_model_params_base.huggingface_model_reference,
    )

    # Create pipeline using ner model and tokenizer
    logger.info("Creating Korean & Japanese NER pipeline")
    hf_pipeline_kj = pipeline(
        task=model_card.ner_model_params_kj.huggingface_pipeline_task_kj,
        model=model_card.ner_model_params_kj.huggingface_model_reference_kj,
        tokenizer=model_card.ner_model_params_kj.huggingface_model_reference_kj,
    )

    # ner settings
    ner_settings_base = model_card.ner_model_params_base.ner_settings.dict()
    ner_settings_kj = model_card.ner_model_params_kj.ner_settings.dict()

    ner_settings = [ner_settings_base, ner_settings_kj]

    # --- create prediction files
    logger.info("Making predictions from example inputs")
    ner_predictions_base: List[List[Dict[str, Union[str, float, int]]]] = hf_pipeline(
        model_card.model_inputs.sample_documents[0]
    )

    ner_predictions_kj: List[List[Dict[str, Union[str, float, int]]]] = hf_pipeline_kj(
        model_card.model_inputs.sample_documents[1]
    )

    # Convert score's value from np.float32 to just float
    # Reason for this is because float32 types are not JSON serializable
    for sublist in ner_predictions_base:
        for dictionary in sublist:
            dictionary["score"] = float(dictionary["score"])

    for sublist in ner_predictions_kj:
        for dictionary in sublist:
            dictionary["score"] = float(dictionary["score"])

    ner_predictions = [ner_predictions_base, ner_predictions_kj]

    # --- add assets to registered model version on neptune ai
    # testing assets - inputs, inference specs and outputs
    logger.info("Pushing assets to neptune AI")
    for (test_file, test_file_attribute_path) in [
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

    hf_pipeline_local_dir_kj = os.path.join(
        model_card.local_output_dir, "hf_pipeline_kj"
    )
    hf_pipeline_kj.save_pretrained(hf_pipeline_local_dir_kj)

    model_version.upload_directory_to_model_version(
        local_directory_path=hf_pipeline_local_dir,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.base_model_subdirectory,
    )

    model_version.upload_directory_to_model_version(
        local_directory_path=hf_pipeline_local_dir_kj,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.kj_model_subdirectory,
    )
    # model card
    model_version.upload_config_to_model_version(
        config=model_card.dict(), neptune_attribute_path="model/model_card"
    )

    model_version.stop()


if __name__ == "__main__":
    main()
