"""Register trained model."""

# Standard Library
import os

# 3rd party libraries
from bertopic import BERTopic
from bertopic.representation import MaximalMarginalRelevance
from cuml.cluster import HDBSCAN
from cuml.manifold import UMAP
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

# Internal libraries
from onclusiveml.nlp.stopwords.helpers import load_stop_words_file
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.fetch_and_upload_dataset import fetch_and_upload
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
    # --- initialize models
    english_stopwords = load_stop_words_file(
        lang=model_card.model_params.stop_words_lang
    )
    vectorizer_model = CountVectorizer(
        stop_words=english_stopwords,
        min_df=model_card.model_params.min_df,
        ngram_range=model_card.model_params.ngram_range,
    )

    cluster_model = HDBSCAN(
        min_cluster_size=model_card.model_params.min_cluster_size,
        metric=model_card.model_params.hdbscan_metric,
        cluster_selection_method=model_card.model_params.cluster_selection_method,
        prediction_data=model_card.model_params.prediction_data,
    )

    umap_model = UMAP(
        n_neighbors=model_card.model_params.n_neighbors,
        n_components=model_card.model_params.n_components,
        min_dist=model_card.model_params.min_dist,
        metric=model_card.model_params.umap_metric,
        random_state=0,
    )

    representation_model = MaximalMarginalRelevance(
        diversity=model_card.model_params.diversity
    )

    topic_model = BERTopic(
        umap_model=umap_model,
        hdbscan_model=cluster_model,
        vectorizer_model=vectorizer_model,
        verbose=model_card.model_params.verbose,
        language=model_card.model_params.language,
        n_gram_range=model_card.model_params.n_gram_range,
        representation_model=representation_model,
    )
    sentence_model = SentenceTransformer(model_card.model_params.embedding_model)
    docs_df, file_key = fetch_and_upload(model_version.get_url().split("/")[-1])
    docs = docs_df["content"].apply(str).values.tolist()
    doc_embeddings = sentence_model.encode(docs, show_progress_bar=True)
    topic_model.fit(documents=docs, embeddings=doc_embeddings)
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
