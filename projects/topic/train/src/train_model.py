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
from src.settings import DataFetchParams

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
        vectorizer_model=vectorizer_model,
        cluster_model=cluster_model,
        umap_model=umap_model,
        representation_model=representation_model,
    )

    bertopic_trainer.initialize_embedding_model()

    bertopic_trainer.initialize_model()

    bertopic_trainer.get_training_data()

    bertopic_trainer.upload_training_data_to_s3()

    bertopic_trainer.train()

    bertopic_trainer.upload_model_version()


if __name__ == "__main__":
    main()
