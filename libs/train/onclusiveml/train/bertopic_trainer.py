from onclusiveml.data.feature_store import FeatureStoreParams

from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedParams,
    TrackedModelVersion
)
from typing import List, Optional

class BertopicTrainer(OnclusiveModelTrainer):
    def __init__(
            self,
            tracked_model_specs : TrackedModelSpecs,
            model_card: TrackedModelCard,
            data_fetch_params: FeatureStoreParams,
            stopwords : List[str],
            vectorizer_model: CountVectorizer,
            cluster_model: HDBSCAN,
            umap_model: UMAP,
            representation_model: MaximalMarginalRelevance)-> None:

        super.__init__(tracked_model_specs=tracked_model_specs,
                    model_card=model_card,
                       data_fetch_params=data_fetch_params)
        self.stopwords = stopwords
        self.vectorizer_model = vectorizer_model
        self.cluster_model = cluster_model
        self.umap_model = umap_model
        self.representation_model = representation_model

    def initialize_embedding_model(self):
        self.sentence_model = SentenceTransformer(self.model_card.model_params.embedding_model)

    def initialize_model(self):
        self.topic_model = BERTopic(
        umap_model=self.umap_model,
        hdbscan_model=self.cluster_model,
        vectorizer_model=self.vectorizer_model,
        verbose=self.model_card.model_params.verbose,
        language=self.model_card.model_params.language,
        n_gram_range=self.model_card.model_params.n_gram_range,
        representation_model=representation_model,
    )

    def embed_training_docs(self):
        self.doc_embeddings = self.sentence_model.encode(self.docs, show_progress_bar=True)

    def train(self):
        self.topic_model.fit(documents=self.docs, embeddings=self.doc_embeddings)