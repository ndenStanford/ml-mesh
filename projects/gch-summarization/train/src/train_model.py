"""Register trained model."""

# Standard Library
import os

# ML libs
from transformers import (
    BartForConditionalGeneration,
    BartTokenizer,
    MBartForConditionalGeneration,
    MBartTokenizer,
    pipeline,
)

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelVersion


logger = get_default_logger(__name__)

# Source
from src.settings import (  # type: ignore[attr-defined]
    TrackedSummarizationModelCard,
    TrackedSummarizationModelSpecs,
)


def main() -> None:
    """Register trained model."""
    model_specs = TrackedSummarizationModelSpecs()
    model_card = TrackedSummarizationModelCard()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # initialize registered model on neptune ai
    model_version = TrackedModelVersion(**model_specs.dict())
    # --- initialize models
    # get pretrained model and tokenizer
    logger.info("Initializing model and tokenizer for English")
    tokenizer_en = BartTokenizer.from_pretrained(
        model_card.model_params_en.huggingface_model_reference_en,
        max_length=512,
        truncate=True,
    )
    model_en = BartForConditionalGeneration.from_pretrained(
        model_card.model_params_en.huggingface_model_reference_en
    )
    hf_pipeline_en = pipeline(
        task=model_card.model_params_en.huggingface_pipeline_task,
        model=model_en,
        tokenizer=tokenizer_en,
    )

    logger.info("Initializing model and tokenizer for French and German")
    tokenizer_frde = MBartTokenizer.from_pretrained(
        model_card.model_params_frde.huggingface_model_reference_frde,
        max_length=512,
        truncate=True,
    )
    model_frde = MBartForConditionalGeneration.from_pretrained(
        model_card.model_params_frde.huggingface_model_reference_frde
    )

    hf_pipeline_frde = pipeline(
        task=model_card.model_params_frde.huggingface_pipeline_task,
        model=model_frde,
        tokenizer=tokenizer_frde,
    )

    logger.info("Initializing model and tokenizer for Spanish")
    tokenizer_es = BartTokenizer.from_pretrained(
        model_card.model_params_es.huggingface_model_reference_es,
        max_length=512,
        truncate=True,
    )
    model_es = BartForConditionalGeneration.from_pretrained(
        model_card.model_params_es.huggingface_model_reference_es
    )

    hf_pipeline_es = pipeline(
        task=model_card.model_params_es.huggingface_pipeline_task,
        model=model_es,
        tokenizer=tokenizer_es,
    )

    logger.info("Initializing model and tokenizer for Catalan")
    tokenizer_ca = BartTokenizer.from_pretrained(
        model_card.model_params_ca.huggingface_model_reference_ca,
        max_length=512,
        truncate=True,
    )
    model_ca = BartForConditionalGeneration.from_pretrained(
        model_card.model_params_ca.huggingface_model_reference_ca
    )

    hf_pipeline_ca = pipeline(
        task=model_card.model_params_ca.huggingface_pipeline_task,
        model=model_ca,
        tokenizer=tokenizer_ca,
    )

    logger.info("Initializing model and tokenizer for Italian")
    tokenizer_it = BartTokenizer.from_pretrained(
        model_card.model_params_it.huggingface_model_reference_it,
        max_length=512,
        truncate=True,
        model_max_length=1024,
    )
    model_it = BartForConditionalGeneration.from_pretrained(
        model_card.model_params_it.huggingface_model_reference_it
    )

    hf_pipeline_it = pipeline(
        task=model_card.model_params_it.huggingface_pipeline_task,
        model=model_it,
        tokenizer=tokenizer_it,
    )

    pipelines = [
        hf_pipeline_en,
        hf_pipeline_frde,
        hf_pipeline_es,
        hf_pipeline_ca,
        hf_pipeline_it,
    ]
    # summarization settings
    summarization_settings_en = model_card.model_params_en.summarization_settings.dict()
    summarization_settings_frde = (
        model_card.model_params_frde.summarization_settings.dict()
    )
    summarization_settings_es = model_card.model_params_es.summarization_settings.dict()
    summarization_settings_ca = model_card.model_params_ca.summarization_settings.dict()
    summarization_settings_it = model_card.model_params_it.summarization_settings.dict()

    summarization_settings = [
        summarization_settings_en,
        summarization_settings_frde,
        summarization_settings_es,
        summarization_settings_ca,
        summarization_settings_it,
    ]
    # --- create prediction files
    # Making predictions from example inputs
    logger.info("Making predictions from example inputs")
    # Tokenize the sample documents
    summarization_predictions = []
    for idx in range(len(summarization_settings)):
        summaries = pipelines[idx](
            model_card.model_inputs.sample_documents[idx],
            min_length=32,
            max_length=128,
            num_beams=1,
        )
        summarization_predictions.append(summaries[0]["summary_text"])
    # --- add assets to registered model version on neptune ai
    # testing assets - inputs, inference specs and outputs
    logger.info("Pushing assets to neptune AI")
    for (test_file, test_file_attribute_path) in [
        (model_card.model_inputs.sample_documents, model_card.model_test_files.inputs),
        (summarization_settings, model_card.model_test_files.inference_params),
        (summarization_predictions, model_card.model_test_files.predictions),
    ]:
        model_version.upload_config_to_model_version(
            config=test_file, neptune_attribute_path=test_file_attribute_path
        )

    logger.info("Pushing model artifact and assets to s3")
    # model artifact
    hf_pipeline_local_dir_en = os.path.join(
        model_card.local_output_dir, "hf_pipeline_en"
    )
    hf_pipeline_local_dir_frde = os.path.join(
        model_card.local_output_dir, "hf_pipeline_frde"
    )
    hf_pipeline_local_dir_es = os.path.join(
        model_card.local_output_dir, "hf_pipeline_es"
    )
    hf_pipeline_local_dir_ca = os.path.join(
        model_card.local_output_dir, "hf_pipeline_ca"
    )
    hf_pipeline_local_dir_it = os.path.join(
        model_card.local_output_dir, "hf_pipeline_it"
    )

    hf_pipeline_en.save_pretrained(hf_pipeline_local_dir_en)
    hf_pipeline_frde.save_pretrained(hf_pipeline_local_dir_frde)
    hf_pipeline_es.save_pretrained(hf_pipeline_local_dir_es)
    hf_pipeline_ca.save_pretrained(hf_pipeline_local_dir_ca)
    hf_pipeline_it.save_pretrained(hf_pipeline_local_dir_it)

    model_version.upload_directory_to_model_version(
        local_directory_path=hf_pipeline_local_dir_en,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.en_model_subdirectory,
    )
    model_version.upload_directory_to_model_version(
        local_directory_path=hf_pipeline_local_dir_frde,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.frde_model_subdirectory,
    )
    model_version.upload_directory_to_model_version(
        local_directory_path=hf_pipeline_local_dir_es,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.es_model_subdirectory,
    )
    model_version.upload_directory_to_model_version(
        local_directory_path=hf_pipeline_local_dir_ca,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.ca_model_subdirectory,
    )
    model_version.upload_directory_to_model_version(
        local_directory_path=hf_pipeline_local_dir_it,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.it_model_subdirectory,
    )
    # model card
    model_version.upload_config_to_model_version(
        config=model_card.dict(), neptune_attribute_path="model/model_card"
    )

    model_version.stop()


if __name__ == "__main__":
    main()
