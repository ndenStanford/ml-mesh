"""Upload trained model to Neptune."""

# Standard Library
import os

# 3rd party libraries
import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Internal libraries
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    TrackedTopicBaseModelCard,
    TrackedTopicModelSpecs,
)


def main() -> None:
    """Register trained model."""
    model_specs = TrackedTopicModelSpecs()
    model_card = TrackedTopicBaseModelCard()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # initialize registered model on neptune ai
    model_version = TrackedModelVersion(**model_specs.dict())

    topic_model = BERTopic.load(
        "src/model_artifacts/",
        embedding_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )
    sentence_model = SentenceTransformer(model_card.model_params.embedding_model)
    docs_df = pd.read_parquet("src/TOPIC-TRAINED-43.parquet")

    docs = docs_df["content"].apply(str).values.tolist()
    doc_embeddings = sentence_model.encode(docs, show_progress_bar=True)

    sample_docs = docs[:15]
    sample_embeddings = doc_embeddings[:15]
    sample_topics, sample_probs = topic_model.transform(
        documents=sample_docs, embeddings=sample_embeddings
    )
    sample_topics = [str(i) for i in sample_topics]
    # --- add assets to registered model version on neptune ai
    # testing assets - inputs, inference specs and outputs
    for (test_file, test_file_attribute_path) in [
        (sample_docs, model_card.model_test_files.inputs),
        (model_card.model_params.dict(), model_card.model_test_files.inference_params),
        (sample_topics, model_card.model_test_files.predictions),
    ]:
        model_version.upload_config_to_model_version(
            config=test_file, neptune_attribute_path=test_file_attribute_path
        )
    # model artifact
    topic_model_local_dir = os.path.join(model_card.local_output_dir, "topic_model/")
    topic_model.save(topic_model_local_dir, serialization="pytorch", save_ctfidf=True)
    topic_model.get_topic_info().sort_values("Count", ascending=False).to_csv(
        f"{topic_model_local_dir}topic_info.csv"
    )

    model_version.upload_directory_to_model_version(
        local_directory_path=topic_model_local_dir,
        neptune_attribute_path=model_card.model_artifact_attribute_path,
    )
    # # model card
    model_version.upload_config_to_model_version(
        config=model_card.dict(), neptune_attribute_path="model/model_card"
    )

    model_version.stop()


if __name__ == "__main__":
    main()
