#!/bin/bash

BERTOPIC_PATH=$1

sed -i '/from umap import UMAP/s/^/#/' "$BERTOPIC_PATH/_bertopic.py" && \
sed -i 's/: UMAP//g' "$BERTOPIC_PATH/_bertopic.py" && \
sed -i ':a;N;$!ba;s/or[[:space:]]\+UMAP([^)]\+self\.low_memory)//' "$BERTOPIC_PATH/_bertopic.py" && \
sed -i '/from umap import UMAP/s/^/#/' "$BERTOPIC_PATH/plotting/_topics.py" && \
sed -i '/embeddings = UMAP(n_neighbors=2, n_components=2, metric='"'"'hellinger'"'"', random_state=42).fit_transform(embeddings)/s/^/#/' "$BERTOPIC_PATH/plotting/_topics.py" && \
sed -i '/embeddings = UMAP(n_neighbors=2, n_components=2, metric='"'"'cosine'"'"', random_state=42).fit_transform(embeddings)/s/^/#/' "$BERTOPIC_PATH/plotting/_topics.py" && \
sed -i '/from umap import UMAP/s/^/#/' "$BERTOPIC_PATH/plotting/_hierarchical_documents.py" && \
sed -i '/umap_model = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='"'"'cosine'"'"').fit(embeddings_to_reduce)/s/^/#/' "$BERTOPIC_PATH/plotting/_hierarchical_documents.py" && \
sed -i 's/embeddings_2d = umap_model.embedding_/pass/' "$BERTOPIC_PATH/plotting/_hierarchical_documents.py" && \
sed -i '/from umap import UMAP/s/^/#/' "$BERTOPIC_PATH/plotting/_documents.py" && \
sed -i '/umap_model = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='"'"'cosine'"'"').fit(embeddings_to_reduce)/s/^/#/' "$BERTOPIC_PATH/plotting/_documents.py" && \
sed -i 's/embeddings_2d = umap_model.embedding_/pass/' "$BERTOPIC_PATH/plotting/_documents.py"
