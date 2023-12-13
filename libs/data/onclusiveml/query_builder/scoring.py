"""Scoring."""

# Standard Library
from typing import Any, Dict, List, Tuple, Union

# 3rd party libraries
import numpy as np
from elasticsearch import Elasticsearch
from scipy.spatial.distance import pdist
from scipy.stats import skew
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import pairwise_distances  # noqa

# Internal libraries
from onclusiveml.query_builder.clustering import hdbscan_clustering
from onclusiveml.query_builder.get_articles import get_query_results
from onclusiveml.query_builder.settings import get_settings


settings = get_settings()


def get_relevance_score(
    scores: List[float], query: Any, init_max_score: int = 50
) -> float:
    """Returns a scaled list of scores with upper limit.

    Args:
        scores (List[float]): List of scores to be scaled.
        max_score (float): Maximum score to be used in scaling. Defaults to 50.

    Returns:
        float: Scaled relevance score.
    With max_score set to 50, resulting scaled scores are approximately:
    Score 5 scaled to 4.56
    Score 10 scaled to 6.10
    Score 20 scaled to 7.74
    Score 30 scaled to 8.73
    Score 40 scaled to 9.44
    Score 50 scaled to 10.0
    """

    def quantify_query_broadness(query: Any) -> float:
        broadness_score: float = 0
        elements_to_process: List[Tuple[Any, float]] = [
            (query, 1)
        ]  # Tuple of (element, depth_factor)

        while elements_to_process:
            element, depth_factor = elements_to_process.pop()

            if isinstance(element, dict):
                # Nested queries reduce the impact on the score
                if "nested" in element:
                    depth_factor *= 0.1
                # Process 'should' clause
                if "should" in element and isinstance(element["should"], list):
                    broadness_score += len(element["should"]) * depth_factor
                # Process 'must_not' clause
                if "must_not" in element and isinstance(element["must_not"], list):
                    broadness_score -= len(element["must_not"]) * depth_factor
                # Process 'must' clause
                if "must" in element and isinstance(element["must"], list):
                    broadness_score -= len(element["must"]) * depth_factor
                # Add nested elements to the processing list with updated depth factor
                elements_to_process.extend(
                    [
                        (value, depth_factor)
                        for key, value in element.items()
                        if isinstance(value, (list, dict))
                    ]
                )

            elif isinstance(element, list):
                # Add list items to the processing list with the same depth factor
                elements_to_process.extend([(item, depth_factor) for item in element])

        return broadness_score

    broadness = quantify_query_broadness(query)
    max_score: float = init_max_score * (1 + broadness)
    constrained_scores: List[float] = [min(score, max_score) for score in scores]
    scaled_relevance: float = np.mean(
        [
            (np.log(score + 1) / np.log(max_score + 1)) * 10
            for score in constrained_scores
        ]
    )
    return scaled_relevance


def get_w_penalization(
    cluster_labels: Any, option: str = "proportion", scaling_power: int = 1
) -> float:
    """Calculate a penalization factor for clustering evaluation.

    Args:
        cluster_labels (np.ndarray): Array containing cluster labels.
        option (str): Type of penalization to apply, either "skewness" or "proportion".
                      Defaults to "proportion".

    Returns:
        float: Penalization factor.
    """
    # skewness emphasizing the presence of larger clusters relative to the majority.
    if option == "skewness":
        # if there is only 1 cluster, the skewness is meaningless
        if len(np.unique(cluster_labels)) == 1:
            w_penalization = 1
        else:
            skewness = skew(cluster_labels)
            # normalize skewness to a range between 0 and 1 using a sigmoid function
            w_penalization = 1 / (1 + np.exp(-abs(skewness)))
    # simply penalize with the proportion of the largest cluster
    elif option == "proportion":
        total_size = len(cluster_labels)
        # the biggest cluster excluding the outlier cluster
        filtered_labels = cluster_labels[cluster_labels != -1]
        biggest_cluster_size = np.unique(filtered_labels, return_counts=True)[1].max()
        proportion = biggest_cluster_size / total_size
        # Apply a power function to scale up the proportion
        w_penalization = np.power(proportion, scaling_power)

    return w_penalization


def get_silhouette_score(embeddings: Any, cluster_labels: Any) -> Union[float, None]:
    """Calculate the normalized silhouette score for clustering evaluation.

    Args:
        embeddings (np.ndarray): Array containing embedded data.
        cluster_labels (np.ndarray): Array containing cluster labels.

    Returns:
        Union[float, None]: Normalized silhouette score if more than one cluster, else None.
    """
    # Check if there are more than 1 cluster (excluding noise)
    unique_labels = np.unique(cluster_labels)
    if len(unique_labels) > 1:
        silhouette_avg = silhouette_score(embeddings, cluster_labels)
        normalized_silhouette = (silhouette_avg + 1) / 2
    else:
        # If there's only one cluster, silhouette score is not defined
        normalized_silhouette = None

    return normalized_silhouette


def get_intra_cluster_similarity(
    embeddings: np.ndarray, cluster_ids: np.ndarray, alpha: float = 0.1
) -> Union[float, None]:
    """Calculate the average intra-cluster similarity for clustering evaluation.

    Args:
        embeddings (np.ndarray): Array containing embedded data.
        cluster_ids (np.ndarray): Array containing cluster IDs.
        metric (str): Distance metric to compute similarity. Defaults to 'cosine'.

    Returns:
        Union[float, None]: Average intra-cluster similarity if clusters exist, else None.
    """
    unique_clusters = set(cluster_ids)
    cluster_similarities = []

    for cluster in unique_clusters:
        cluster_embeddings = np.array(
            [embeddings[i] for i, cid in enumerate(cluster_ids) if cid == cluster]
        )
        cluster_size = len(cluster_embeddings)

        if cluster_size > 1:
            # Compute pairwise Manhattan distances and then calculate the average
            distances = pdist(cluster_embeddings, "cityblock")
            avg_distance = np.mean(distances)
            # Scale down the avg_distance for larger clusters
            # The scaling factor decreases as the cluster size increases
            scaling_factor = 1 / np.log(cluster_size)
            scaled_avg_distance = avg_distance * scaling_factor
            # Normalize the similarity to be between 0 and 1
            similarity = 1 / (1 + alpha * scaled_avg_distance)
            cluster_similarities.append(similarity)

    if cluster_similarities:
        overall_average_similarity = np.mean(cluster_similarities)
    else:
        overall_average_similarity = np.nan

    return overall_average_similarity


def get_homogeneity_score(
    embeddings: Any,
    cluster_labels: Any,
    w_silhouette: float,
    w_intra_cluster: float,
    option: str = "skewness",
    penalty_scaling_power: int = 1,
) -> Dict[str, Union[float, None]]:
    """Calculate the homogeneity score.

    Args:
        embeddings (np.ndarray): Array containing embedded data.
        cluster_labels (np.ndarray): Array containing cluster labels.
        w_silhouette (float): Weight for silhouette score.
        w_intra_cluster (float): Weight for intra-cluster similarity.
        option (str): Type of penalization to apply. Defaults to "skewness".

    Returns:
        Dict[str, Union[float, None]]: Dictionary containing silhouette,
        intra-cluster similarity,
        penalization, and homogeneity score.
    """
    # Filter out noise points (labeled as -1)
    filtered_labels = cluster_labels[cluster_labels != -1]
    filtered_embeddings = embeddings[cluster_labels != -1]
    unique_labels = np.unique(filtered_labels)
    # Calculate silhouette score
    silhouette = get_silhouette_score(filtered_embeddings, filtered_labels)
    # Calculate intra-cluster similarity
    intra_cluster_similarity = get_intra_cluster_similarity(
        filtered_embeddings, filtered_labels, alpha=0.1
    )
    if len(unique_labels) > 1:
        # Weighted sum of silhouette score and intra-cluster similarity
        if silhouette is not None and intra_cluster_similarity is not None:
            weighted_homogeneity = (
                w_silhouette * silhouette + w_intra_cluster * intra_cluster_similarity
            )

    # If there's only one cluster, silhouette score is not defined, use intra-cluster only
    elif len(unique_labels) == 1 and intra_cluster_similarity is not None:
        weighted_homogeneity = intra_cluster_similarity
    # Penalize the homogeneity
    w_penalization = get_w_penalization(
        cluster_labels, option=option, scaling_power=penalty_scaling_power
    )
    penalized_homogeneity = weighted_homogeneity * w_penalization
    # Scale the weighted homogeneity to a 0-10 range
    scaled_homogeneity = penalized_homogeneity * 10

    homogeneity_scores = {
        "silhouette": silhouette,
        "intra_cluster_similarity": intra_cluster_similarity,
        "w_penalization": w_penalization,
        "homogeneity_score": scaled_homogeneity,
    }
    return homogeneity_scores


def get_overall_quality_score(
    query: Any,
    list_scores: List[float],
    embeddings: Any,
    cluster_labels: Any,
    w_silhouette: float,
    w_intra_cluster: float,
    w_relevance: float,
    w_homogeneity: float,
    option: str = "skewness",
    penalty_scaling_power: int = 1,
) -> Dict[str, Union[float, None]]:
    """Calculate the overall quality score based on relevance and homogeneity.

    Args:
        list_scores (List[float]): List of scores for relevance.
        embeddings (np.ndarray): Array containing embedded data.
        cluster_labels (np.ndarray): Array containing cluster labels.
        w_silhouette (float): Weight for silhouette score.
        w_intra_cluster (float): Weight for intra-cluster similarity.
        w_relevance (float): Weight for relevance score.
        w_homogeneity (float): Weight for homogeneity score.
        option (str): Type of penalization to apply. Defaults to "skewness".

    Returns:
        Dict[str, Union[float, None]]: Dictionary containing relevance score, homogeneity scores,
                                       and overall quality score.
    """
    relevance_score = get_relevance_score(list_scores, query, init_max_score=50)
    homogeneity_scores = get_homogeneity_score(
        embeddings,
        cluster_labels,
        w_silhouette=w_silhouette,
        w_intra_cluster=w_intra_cluster,
        option=option,
        penalty_scaling_power=penalty_scaling_power,
    )
    if (
        relevance_score is not None
        and homogeneity_scores["homogeneity_score"] is not None
    ):
        overall_quality_score = (
            w_relevance * relevance_score
            + w_homogeneity * homogeneity_scores["homogeneity_score"]
        )
    else:
        overall_quality_score = 0

    all_scores = homogeneity_scores
    all_scores.update({"relevance_score": relevance_score})
    all_scores.update({"overall_quality_score": overall_quality_score})

    return all_scores


def evaluate_query(
    es: Elasticsearch,
    es_index: List[str],
    query: Any,
    clustering_config: Any,
    scoring_config: Any,
) -> Tuple[Dict[str, Union[float, None]], Any, Any, Any]:
    """Evaluate the query and return quality scores, inputs, embeddings, and cluster labels.

    Args:
        es (Elasticsearch): Elasticsearch instance.
        query (str): Query string to evaluate.
        clustering_config (Dict[str, Union[str, int, bool]]): parameters for clustering.
        scoring_config (Dict[str, float]): parameters for scoring.

    Returns:
         Quality scores, inputs, embeddings, and cluster labels.
    """
    inputs, list_scores = get_query_results(es, es_index, query)

    embeddings, cluster_labels = hdbscan_clustering(
        inputs=inputs,
        embedding_method=clustering_config.embedding_method,
        model_path=clustering_config.model_path,
        tfidf_max_features=clustering_config.tfidf_max_features,
        dimension_reduction_method=clustering_config.dimension_reduction_method,
        n_components=clustering_config.n_components,
        umap_n_neighbors=clustering_config.umap_n_neighbors,
        umap_min_dist=clustering_config.umap_min_dist,
        hdbscan_min_cluster_size=clustering_config.hdbscan_min_cluster_size,
        gen_min_span_tree=clustering_config.gen_min_span_tree,
        hdbscan_algorithm=clustering_config.hdbscan_algorithm,
        hdbscan_metric=clustering_config.hdbscan_metric,
        hdbscan_cluster_selection_method=clustering_config.hdbscan_cluster_selection_method,
        hdbscan_allow_single_cluster=clustering_config.hdbscan_allow_single_cluster,
        random_state=2,
    )

    all_scores = get_overall_quality_score(
        query=query,
        list_scores=list_scores,
        embeddings=embeddings,
        cluster_labels=cluster_labels,
        w_silhouette=scoring_config.w_silhouette,
        w_intra_cluster=scoring_config.w_intra_cluster,
        w_relevance=scoring_config.w_relevance,
        w_homogeneity=scoring_config.w_homogeneity,
        option=scoring_config.penalty_option,
        penalty_scaling_power=scoring_config.penalty_scaling_power,
    )

    return all_scores, inputs, embeddings, cluster_labels
