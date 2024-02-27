"""Train IPTC models."""

# Standard Library
import os

# ML libs
from transformers import AutoModelForSequenceClassification

# 3rd party libraries
import boto3
import pandas as pd

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelVersion


logger = get_default_logger(__name__)

# Source
from src.dataset import IPTCDataset
from src.settings import (  # type: ignore[attr-defined]
    BaseTrackedModelSpecs,
    TrackedIPTCBaseModelCard,
)
from src.trainer import IPTCTrainer


def main() -> None:
    """Execute the training process."""
    tracked_model_specs = BaseTrackedModelSpecs()
    model_card = TrackedIPTCBaseModelCard()
    # get data from s3
    logger.info("Getting data from sagemaker S3 bucket")
    sagemaker_bucket = boto3.resource("s3").Bucket(model_card.remote_data_bucket)
    sagemaker_bucket.download_file(
        model_card.train_data_prefix, model_card.local_train_data_path
    )
    sagemaker_bucket.download_file(
        model_card.eval_data_prefix, model_card.local_eval_data_path
    )
    # preprocess dataset
    df_train = pd.read_csv(os.path.join(".", model_card.local_train_data_path))
    df_eval = pd.read_csv(os.path.join(".", model_card.local_eval_data_path))
    train_dataset = IPTCDataset(
        df_train,
        model_card.tokenizer,
        model_card.level,
        model_card.selected_text,
        model_card.first_level_root,
        model_card.second_level_root,
    )
    eval_dataset = IPTCDataset(
        df_eval,
        model_card.tokenizer,
        model_card.level,
        model_card.selected_text,
        model_card.first_level_root,
        model_card.second_level_root,
    )
    # Start the training
    trainer = IPTCTrainer(train_dataset, eval_dataset, model_card, tracked_model_specs)
    trainer()
    # register models to neptune
    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # initialize registered model on neptune ai
    model_version = TrackedModelVersion(**tracked_model_specs.dict())

    iptc_model = AutoModelForSequenceClassification.from_pretrained(
        model_card.local_output_dir
    )
    sample_docs = model_card.model_inputs.sample_documents
    sample_prediction = trainer.predict()
    # --- add assets to registered model version on neptune ai
    # testing assets - inputs, inference specs and outputs
    for (test_file, test_file_attribute_path) in [
        (sample_docs, model_card.model_test_files.inputs),
        (model_card.model_params.dict(), model_card.model_test_files.inference_params),
        (sample_prediction, model_card.model_test_files.predictions),
    ]:
        model_version.upload_config_to_model_version(
            config=test_file, neptune_attribute_path=test_file_attribute_path
        )
    # model artifact
    iptc_model_local_dir = os.path.join(
        model_card.local_output_dir, "iptc_model_artifacts/"
    )
    iptc_model.save(iptc_model_local_dir, serialization="pytorch", save_ctfidf=True)
    iptc_model.get_iptc_info().sort_values("Count", ascending=False).to_csv(
        f"{iptc_model_local_dir}iptc_info.csv"
    )

    model_version.upload_directory_to_model_version(
        local_directory_path=iptc_model_local_dir,
        neptune_attribute_path=model_card.model_artifact_attribute_path,
    )
    # # model card
    model_version.upload_config_to_model_version(
        config=model_card.dict(), neptune_attribute_path="model/model_card"
    )

    model_version.stop()


if __name__ == "__main__":
    main()
