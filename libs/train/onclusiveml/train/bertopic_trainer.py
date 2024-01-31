"""Class for training and managing BERTopic models."""

# Standard Library
import os
from typing import List

# 3rd party libraries
import numpy as np
from bertopic import BERTopic
from bertopic.representation import MaximalMarginalRelevance
from cuml.cluster import HDBSCAN
from cuml.manifold import UMAP
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams
from onclusiveml.tracking import TrackedModelCard, TrackedModelSpecs
from onclusiveml.train.onclusive_model_trainer import OnclusiveModelTrainer


class BertopicTrainer(OnclusiveModelTrainer):
    """Class for training and managing BERTopic models."""

    def __init__(
        self,
        tracked_model_specs: TrackedModelSpecs,
        model_card: TrackedModelCard,
        data_fetch_params: FeatureStoreParams,
        stopwords: List[str],
    ) -> None:
        """Initialize the BertopicTrainer.

        Args:
            tracked_model_specs (TrackedModelSpecs): Specifications for tracked model on neptune.
            model_card (TrackedModelCard): Model card with specifications of the model.
            data_fetch_params (FeatureStoreParams): Parameters for fetching data from feature store.
            stopwords (List[str]): List of stopwords to be used in text processing.

        Returns: None
        """
        self.stopwords = stopwords

        super().__init__(
            tracked_model_specs=tracked_model_specs,
            model_card=model_card,
            data_fetch_params=data_fetch_params,
        )

    def initialize_embedding_model(self) -> None:
        """Initialize the sentence embedding model.

        Returns: None
        """
        self.sentence_model = SentenceTransformer(
            self.model_card.model_params.embedding_model
        )

    def initialize_model(self) -> None:
        """Initialize the BERTopic model.

        Returns: None
        """
        self.initialize_embedding_model()

        vectorizer_model = CountVectorizer(
            stop_words=self.stopwords,
            min_df=self.model_card.model_params.min_df,
            ngram_range=self.model_card.model_params.ngram_range,
        )

        cluster_model = HDBSCAN(
            min_cluster_size=self.model_card.model_params.min_cluster_size,
            metric=self.model_card.model_params.hdbscan_metric,
            cluster_selection_method=self.model_card.model_params.cluster_selection_method,
            prediction_data=self.model_card.model_params.prediction_data,
        )

        umap_model = UMAP(
            n_neighbors=self.model_card.model_params.n_neighbors,
            n_components=self.model_card.model_params.n_components,
            min_dist=self.model_card.model_params.min_dist,
            metric=self.model_card.model_params.umap_metric,
            random_state=0,
        )

        representation_model = MaximalMarginalRelevance(
            diversity=self.model_card.model_params.diversity
        )

        self.topic_model = BERTopic(
            umap_model=umap_model,
            hdbscan_model=cluster_model,
            vectorizer_model=vectorizer_model,
            verbose=self.model_card.model_params.verbose,
            language=self.model_card.model_params.language,
            n_gram_range=self.model_card.model_params.n_gram_range,
            representation_model=representation_model,
        )

    def embed_training_docs(self) -> None:
        """Embed training documents using the sentence embedding model.

        Returns: None
        """
        self.doc_embeddings = self.sentence_model.encode(
            self.docs, show_progress_bar=True
        )

    def train(self) -> None:
        """Train the BERTopic model using the embedded training documents.

        Returns: None
        """
        self.embed_training_docs()
        self.topic_model.fit(documents=self.docs, embeddings=self.doc_embeddings)

    def predict(self, docs: List[str], embeddings: np.ndarray) -> List[str]:
        """Make predictions using the trained BERTopic model.

        Args:
            docs (List[str]): List of documents to predict topics for.
            embeddings (np.ndarray): Embeddings of the input documents.

        Returns:
            List[str]: List of predicted topic labels for the input documents.
        """
        topics, _ = self.topic_model.transform(documents=docs, embeddings=embeddings)
        return [str(i) for i in topics]

    def save(self) -> None:
        """Save the trained BERTopic model and related information locally.

        Returns: None
        """
        self.topic_model_local_dir = os.path.join(
            self.model_card.local_output_dir, "topic_model/"
        )
        self.topic_model.save(
            self.topic_model_local_dir, serialization="pytorch", save_ctfidf=True
        )
        self.topic_model.get_topic_info().sort_values("Count", ascending=False).to_csv(
            f"{self.topic_model_local_dir}topic_info.csv"
        )
