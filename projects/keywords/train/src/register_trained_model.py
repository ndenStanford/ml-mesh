"""Register trained model."""

# Standard Library
import os
from typing import List, Tuple

# ML libs
from keybert import KeyBERT
from transformers import pipeline

# Internal libraries
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    TrackedKeywordModelSpecs,
    TrackedKeywordsBaseModelCard,
)


def main() -> None:
    """Register trained model."""
    model_specs = TrackedKeywordModelSpecs()
    model_card = TrackedKeywordsBaseModelCard()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # initialize registered model on neptune ai
    model_version = TrackedModelVersion(**model_specs.dict())
    # --- initialize models
    # get specified huggingface transformer pipeline
    hf_pipeline = pipeline(
        task=model_card.model_params.huggingface_pipeline_task,
        model=model_card.model_params.huggingface_model_reference,
    )
    # initialize keybert model with huggingface pipeline backend
    keybert_model = KeyBERT(model=hf_pipeline)
    # --- create prediction files
    # keybert model
    # list of tuples (ngram/word, prob)
    keyword_extraction_settings = (
        model_card.model_params.keyword_extraction_settings.dict()
    )

    keybert_predictions: List[Tuple[str, float]] = keybert_model.extract_keywords(
        model_card.model_inputs.sample_documents, **keyword_extraction_settings
    )
    # --- add assets to registered model version on neptune ai
    # testing assets - inputs, inference specs and outputs
    for (test_file, test_file_attribute_path) in [
        (model_card.model_inputs.sample_documents, model_card.model_test_files.inputs),
        (keyword_extraction_settings, model_card.model_test_files.inference_params),
        (keybert_predictions, model_card.model_test_files.predictions),
    ]:
        model_version.upload_config_to_model_version(
            config=test_file, neptune_attribute_path=test_file_attribute_path
        )
    # model artifact
    hf_pipeline_local_dir = os.path.join(model_card.local_output_dir, "hf_pipeline")
    hf_pipeline.save_pretrained(hf_pipeline_local_dir)

    model_version.upload_directory_to_model_version(
        local_directory_path=hf_pipeline_local_dir,
        neptune_attribute_path=model_card.model_artifact_attribute_path,
    )
    # # model card
    model_version.upload_config_to_model_version(
        config=model_card.dict(), neptune_attribute_path="model/model_card"
    )

    model_version.stop()


if __name__ == "__main__":
    main()
