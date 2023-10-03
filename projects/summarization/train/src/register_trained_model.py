"""Register trained model."""

# Standard Library
import os
from typing import Dict, List, Union

# ML libs
from transformers import AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments
from transformers import pipeline, MBartTokenizer, BartTokenizer, AutoTokenizer
from transformers import MBartForConditionalGeneration, BartForConditionalGeneration

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelVersion


logger = get_default_logger(__name__)

# Source
from src.settings import (  # type: ignore[attr-defined]
    TrackedSumModelCard,
    TrackedSumModelSpecs,
)


def main() -> None:
    """Register trained model."""
    model_specs = TrackedSumModelSpecs()
    model_card = TrackedSumModelCard()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # initialize registered model on neptune ai
    model_version = TrackedModelVersion(**model_specs.dict())
    # --- initialize models
    # get pretrained model and tokenizer
    logger.info("Initializing model and tokenizer for English")
    tokenizer_en = AutoTokenizer.from_pretrained(
        model_card.SumModelParamsEn.huggingface_model_reference
    )
    model_en = AutoModelForSeq2SeqLM.from_pretrained(
        model_card.SumModelParamsEn.huggingface_model_reference, return_dict=False
    )
    
    logger.info("Initializing model and tokenizer for French and German")
    tokenizer_frde = AutoTokenizer.from_pretrained(
        model_card.SumModelParamsFrDe.huggingface_model_reference
    )
    model_frde = AutoModelForSeq2SeqLM.from_pretrained(
        model_card.SumModelParamsFrDe.huggingface_model_reference, return_dict=False
    )
    
    logger.info("Initializing model and tokenizer for Spanish")
    tokenizer_es = AutoTokenizer.from_pretrained(
        model_card.SumModelParamsEs.huggingface_model_reference
    )
    model_es = AutoModelForSeq2SeqLM.from_pretrained(
        model_card.SumModelParamsEs.huggingface_model_reference, return_dict=False
    )
    
    logger.info("Initializing model and tokenizer for Catalan")
    tokenizer_ca = AutoTokenizer.from_pretrained(
        model_card.SumModelParamsCa.huggingface_model_reference
    )
    model_ca = AutoModelForSeq2SeqLM.from_pretrained(
        model_card.SumModelParamsCa.huggingface_model_reference, return_dict=False
    )
    
    logger.info("Initializing model and tokenizer for Italian")
    tokenizer_it = AutoTokenizer.from_pretrained(
        model_card.SumModelParamsIt.huggingface_model_reference
    )
    model_it = AutoModelForSeq2SeqLM.from_pretrained(
        model_card.SumModelParamsIt.huggingface_model_reference, return_dict=False
    )
    
    # summarization settings
    sum_settings_en = model_card.model_params_en.sum_settings.dict()
    sum_settings_frde = model_card.model_params_frde.sum_settings.dict()
    sum_settings_es = model_card.model_params_es.sum_settings.dict()
    sum_settings_ca = model_card.model_params_ca.sum_settings.dict()
    sum_settings_it = model_card.model_params_it.sum_settings.dict()
    
    
    # --- create prediction files    
    # Making predictions from example inputs
    logger.info("Making predictions from example inputs")
    
    # Tokenize the sample documents
    inputs = tokenizer_en.batch_encode_plus(
        model_card.model_inputs.sample_documents,
        return_tensors="pt",
        truncation=True,
        padding="longest",
        max_length=512
    )
    
    # Generate summaries
    summaries = model_en.generate(**inputs)
    
    # Decode the summaries
    sum_predictions = [tokenizer_en.decode(summary, skip_special_tokens=True) for summary in summaries]
    
    # --- add assets to registered model version on neptune ai
    # testing assets - inputs, inference specs and outputs
    logger.info("Pushing assets to neptune AI")
    for (test_file, test_file_attribute_path) in [
        (model_card.model_inputs.sample_documents, model_card.model_test_files.inputs),
        (sum_settings_en, model_card.model_test_files.inference_params),
        (sum_predictions, model_card.model_test_files.predictions),
    ]:
        model_version.upload_config_to_model_version(
            config=test_file, neptune_attribute_path=test_file_attribute_path
        )

    logger.info("Pushing model artifact and assets to s3")
    # model artifact
    hf_model_local_dir_en = os.path.join(model_card.local_output_dir, "hf_model_en")
    hf_model_local_dir_frde = os.path.join(model_card.local_output_dir, "hf_model_frde")
    hf_model_local_dir_es = os.path.join(model_card.local_output_dir, "hf_model_es")
    hf_model_local_dir_ca = os.path.join(model_card.local_output_dir, "hf_model_ca")
    hf_model_local_dir_it = os.path.join(model_card.local_output_dir, "hf_model_it")
    
    model_en.save_pretrained(hf_model_local_dir_en)
    model_frde.save_pretrained(hf_model_local_dir_frde)
    model_es.save_pretrained(hf_model_local_dir_es)
    model_ca.save_pretrained(hf_model_local_dir_ca)
    model_it.save_pretrained(hf_model_local_dir_it)

    model_version.upload_directory_to_model_version(
        local_directory_path=hf_model_local_dir_en,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.en_model_subdirectory,
    )
    model_version.upload_directory_to_model_version(
        local_directory_path=hf_model_local_dir_frde,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.frde_model_subdirectory,
    )
    model_version.upload_directory_to_model_version(
        local_directory_path=hf_model_local_dir_es,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.es_model_subdirectory,
    )
    model_version.upload_directory_to_model_version(
        local_directory_path=hf_model_local_dir_ca,
        neptune_attribute_path=model_card.model_artifact_attribute_path
        + model_card.ca_model_subdirectory,
    )
    model_version.upload_directory_to_model_version(
        local_directory_path=hf_model_local_dir_it,
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