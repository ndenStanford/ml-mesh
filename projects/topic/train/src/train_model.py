"""Register trained model."""

# Standard Library
import os

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.stopwords.helpers import load_stop_words_file
from onclusiveml.train import BertopicTrainer

# Source
from src.settings import (  # type: ignore[attr-defined]
    DataFetchParams,
    TrackedTopicBaseModelCard,
    TrackedTopicModelSpecs,
)


logger = get_default_logger(__name__)


def main() -> None:
    """Register trained model."""
    model_specs = TrackedTopicModelSpecs()
    model_card = TrackedTopicBaseModelCard()
    data_fetch_params = DataFetchParams()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)

    stopwords = load_stop_words_file(lang=model_card.model_params.stop_words_lang)

    bertopic_trainer = BertopicTrainer(
        tracked_model_specs=model_specs,
        model_card=model_card,
        data_fetch_params=data_fetch_params,
        stopwords=stopwords,
    )

    bertopic_trainer.get_training_data()

    bertopic_trainer.upload_training_data_to_s3()

    logger.info(
        f"Training data uploaded to s3 location : {bertopic_trainer.full_file_key}"
    )

    bertopic_trainer.initialize_model()

    bertopic_trainer.train()

    bertopic_trainer.save()
    if data_fetch_params.save_artifact:
        sample_docs = bertopic_trainer.docs[:15]
        sample_embeddings = bertopic_trainer.doc_embeddings[:15]

        sample_topics = bertopic_trainer.predict(sample_docs, sample_embeddings)

        bertopic_trainer.upload_model_to_neptune(
            [sample_docs, model_card.model_params.dict(), sample_topics],
            [
                model_card.model_test_files.inputs,
                model_card.model_test_files.inference_params,
                model_card.model_test_files.predictions,
            ],
            bertopic_trainer.topic_model_local_dir,
        )


if __name__ == "__main__":
    main()
