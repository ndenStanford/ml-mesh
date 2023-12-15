"""Query builder."""

# Standard Library
from typing import Any, List

# ML libs
from transformers import AutoTokenizer

# 3rd party libraries
import hdbscan
import umap.umap_ as umap
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer


# feature extraction with tfidf
def get_tfidf_embedding(inputs: List[str], max_features: int = 1000) -> Any:
    """Returns the tfidf embeddings.

    Args:
        inputs (List[str]): the list of texts we got from elasticsearch.
        max_features (int): the max features of the matrix

    Returns:
        tfidf embeddings.
    """
    tfidf_vectorizer = TfidfVectorizer(max_features=max_features)
    tfidf_embeddings = tfidf_vectorizer.fit_transform(inputs)

    return tfidf_embeddings


# feature extraction with pretrained
def get_pretrained_embedding(
    inputs: List[str], model_path: str = "xlm-roberta-base"
) -> Any:
    """Returns the pretrained embeddings.

    Args:
        inputs (List[str]): the list of texts we got from elasticsearch.
        model_path (str): the name of the pretrained model

    Returns:
        pretrained embeddings.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    pretrained_embeddings = tokenizer(
        inputs, max_length=512, padding=True, truncation=True, return_tensors="pt"
    )["input_ids"].numpy()
    return pretrained_embeddings


def reduce_dimension_pca(
    embeddings: Any, n_components: int = 10, random_state: int = 1
) -> Any:
    """Returns the truncatedSVD embeddings.

    Args:
        embeddings: the embedded texts.
        n_componenents (int): the number of components to which the data should be reduced
        random_state (int): set the random seed for reproducibility

    Returns:
        truncatedSVD_embeddings.
    """
    # Initialize PCA
    pca = PCA(n_components=n_components, random_state=1)
    pca_embeddings = pca.fit_transform(embeddings)
    return pca_embeddings


def reduce_dimension_truncatedSVD(
    embeddings: Any, n_components: int = 10, random_state: int = 1
) -> Any:
    """Returns the truncated truncatedSVD embeddings.

    Args:
        embeddings: the embedded texts.
        n_componenents (int): the number of components to which the data should be reduced
        random_state (int): set the random seed for reproducibility

    Returns:
        truncated truncatedSVD_embeddings.
    """
    svd = TruncatedSVD(n_components=n_components, random_state=1)
    truncatedSVD_embeddings = svd.fit_transform(embeddings)

    return truncatedSVD_embeddings


# dimension reduction with umap
def reduce_dimension_umap(
    embeddings: Any,
    n_components: int = 2,
    n_neighbors: int = 15,
    min_dist: float = 0.1,
    metric: str = "cosine",
    random_state: int = 1,
) -> Any:
    """Returns the umap embeddings.

    Args:
        embeddings: the embedded texts.
        n_componenents (int): defines the number of components to which the data should be reduced
        n_neighbors (int): the number of minimum neighbors for dimension reduction
        min_dist (float): the minimum distance to consder a data point as a neighbor
        metric (str): method used to compute the distances
        random_state (int): set the random seed for reproducibility

    Returns:
        Returns umap embeddings.
    """
    umap_model = umap.UMAP(
        n_components=n_components,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric=metric,
        random_state=random_state,
    )
    umap_embedding = umap_model.fit_transform(embeddings)

    return umap_embedding


# clustering with hdbscan
def hdbscan_clustering(
    inputs: List[str],
    embedding_method: str = "pretrained",
    model_path: str = "xlm-roberta-base",
    tfidf_max_features: int = 4000,
    dimension_reduction_method: str = "umap",
    n_components: int = 10,
    umap_n_neighbors: int = 15,
    umap_min_dist: float = 0.1,
    hdbscan_min_cluster_size: int = 5,
    gen_min_span_tree: bool = True,
    hdbscan_algorithm: str = "generic",
    hdbscan_metric: str = "euclidean",
    hdbscan_cluster_selection_method: str = "eom",
    hdbscan_allow_single_cluster: bool = True,
    random_state: int = 1,
) -> Any:
    """Returns the final embeddings with cluster labels.

    Args:
        inputs (List[str]): list of texts
        embedding_method(str): name of the embedding method
        model_path(str): name of the pretrained model
        tfidf_max_features(int): max number of features for the tfidf matrix
        dimension_reduction_method(str): name of the dimension reduction method
        n_components(int): the number of components to which the data should be reduced
        umap_n_neighbors (int): the number of minimum neighbors for dimension reduction
        umap_min_dist (float): the minimum distance to consder a data point as a neighbor
        hdbscan_min_cluster_size: (int): the number of minimum neighbors to form a cluster
        gen_min_span_tree(boll)
        hdbscan_metric(str)
        hdbscan_cluster_selection_method(str)
        hdbscan_allow_single_cluster(bool)
        random_state(int)

    Returns:
        Returns the final embeddings with cluster labels.
    """
    if embedding_method == "pretrained":
        embeddings = get_pretrained_embedding(inputs, model_path)
    elif embedding_method == "tfidf":
        embeddings = get_tfidf_embedding(inputs, max_features=tfidf_max_features)

    if dimension_reduction_method == "umap":
        embeddings = reduce_dimension_umap(
            embeddings,
            n_components=n_components,
            n_neighbors=umap_n_neighbors,
            min_dist=umap_min_dist,
            metric="cosine",
            random_state=random_state,
        )
    elif dimension_reduction_method == "pca":
        embeddings = reduce_dimension_pca(
            embeddings, n_components=n_components, random_state=random_state
        )
    elif dimension_reduction_method == "truncatedSVD":
        embeddings = reduce_dimension_truncatedSVD(
            embeddings, n_components=n_components, random_state=random_state
        )

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=hdbscan_min_cluster_size,
        gen_min_span_tree=gen_min_span_tree,
        algorithm=hdbscan_algorithm,
        metric=hdbscan_metric,
        cluster_selection_method=hdbscan_cluster_selection_method,
        allow_single_cluster=hdbscan_allow_single_cluster,
    )

    clusterer.fit(embeddings)
    cluster_labels = clusterer.labels_

    return embeddings, cluster_labels
