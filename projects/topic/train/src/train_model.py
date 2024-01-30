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
    data_fetch_params = DataFetchParams()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)

    stopwords = load_stop_words_file(
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

    bertopic_trainer = BertopicTrainer(tracked_model_specs = model_specs,
                                       model_card = model_card,
                                       data_fetch_params = data_fetch_params,
                                       stopwords = stopwords,
                                       vectorizer_model = vectorizer_model,
                                       cluster_model = cluster_model,
                                       umap_model = umap_model,
                                       representation_model = representation_model)

    bertopic_trainer.initialize_embedding_model()

    bertopic_trainer.initialize_model()

    bertopic_trainer.get_training_data()

    bertopic_trainer.upload_training_data_to_s3()

    bertopic_trainer.train()

    bertopic_trainer.upload_model_version()

if __name__ == "__main__":
    main()
