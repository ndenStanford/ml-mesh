# Standard Library
from typing import Dict

# ML libs
from transformers import pipeline

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.models.keywords import CompiledKeyBERT
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (
    DocumentPipelineCompilationSettings,
    IOSettings,
    UncompiledTrackedModelSpecs,
    WordPipelineCompilationSettings,
)


def main() -> None:
    # get read-only base model version
    base_model_specs = UncompiledTrackedModelSpecs()
    base_model_version = TrackedModelVersion(**base_model_specs.dict())
    # get base model card
    io_settings = IOSettings()
    base_model_card: Dict = base_model_version.download_config_from_model_version(
        "model/model_card"
    )
    # re-load base model pipeline
    base_model_pipeline = pipeline(
        task=base_model_card["model_params"]["huggingface_pipeline_task"],
        model=io_settings.download.model_directory,
    )
    # compile base model pipeline for word embedding feature extraction
    compiled_word_embedding_pipeline = CompiledPipeline.from_pipeline(
        pipeline=base_model_pipeline,
        **WordPipelineCompilationSettings().dict(exclude={"pipeline_name"})
    )
    # compile base model pipeline for document embedding feature extraction
    compiled_document_embedding_pipeline = CompiledPipeline.from_pipeline(
        pipeline=base_model_pipeline,
        **DocumentPipelineCompilationSettings().dict(exclude={"pipeline_name"})
    )
    # create compiled keybert model
    compiled_keybert = CompiledKeyBERT(
        document_pipeline=compiled_document_embedding_pipeline,
        compiled_word_pipeline=compiled_word_embedding_pipeline,
    )

    print(io_settings.compile.model_directory)
    # export compiled keybert model for next workflow component: test
    compiled_keybert.save_pretrained(io_settings.compile.model_directory)


if __name__ == "__main__":
    main()
