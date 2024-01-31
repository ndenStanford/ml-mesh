
# Standard Library
from typing import List, Optional

# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedModelVersion,
    TrackedParams,
)
from onclusiveml.train.onclusive_model_trainer import OnclusiveModelTrainer
from bertopic import BERTopic
from bertopic.representation import MaximalMarginalRelevance
from cuml.cluster import HDBSCAN
from cuml.manifold import UMAP
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

class BertopicTrainer(OnclusiveModelTrainer):
    def __init__(
        self,
        tracked_model_specs: TrackedModelSpecs,
        model_card: TrackedModelCard,
        data_fetch_params: FeatureStoreParams,
        stopwords: List[str],
    ) -> None:

        self.stopwords = stopwords
        
        super().__init__(
            tracked_model_specs=tracked_model_specs,
            model_card=model_card,
            data_fetch_params=data_fetch_params,
        )

    def initialize_embedding_model(self):
        self.sentence_model = SentenceTransformer(
            self.model_card.model_params.embedding_model
        )

    def initialize_model(self):
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

    def embed_training_docs(self):
        self.doc_embeddings = self.sentence_model.encode(
            self.docs, show_progress_bar=True
        )

    def train(self):
        self.embed_training_docs()
        self.topic_model.fit(documents=self.docs, embeddings=self.doc_embeddings)
