"""Utility functions for data imputation, data processing, and scikit-learn pipelines."""

# Standard Library
from collections import defaultdict

# 3rd party libraries
import numpy as np
import pandas as pd
import yaml
from sklearn.base import BaseEstimator, TransformerMixin


def read_yaml(yaml_str):
    """Parse a YAML string into a Python object.

    Args:
        yaml_str (str): The YAML string to parse.

    Returns:
        list: The parsed YAML data as a Python object (usually a dictionary or list).
              If the input is invalid or an error occurs, returns an empty list.
    """
    try:
        return (
            yaml.safe_load(yaml_str) if yaml_str and isinstance(yaml_str, str) else []
        )
    except yaml.YAMLError:
        # print(f"Error parsing YAML: {e}")
        return []


def imprec(intervaltimes, metadatawindows, metadata_old):
    """Impute metadata for missing intervals based on surrounding metadata windows.

    Args:
        intervaltimes (list): List of time intervals where metadata needs to be imputed.
        metadatawindows (list): List of tuples, where each tuple contains two metadata windows.
        metadata_old (list): Metadata to use when no new metadata is available.

    Returns:
        list: List of tuples containing the time and the imputed metadata.
    """
    acc = []
    while intervaltimes:
        if not metadatawindows:
            acc += [(t, metadata_old) for t in intervaltimes]
            break
        (tmd1, md1), (tmd2, md2) = metadatawindows[0]
        interval_times, intervaltimes = [t for t in intervaltimes if t < tmd2], [
            t for t in intervaltimes if t >= tmd2
        ]
        interval_size = (tmd2 - tmd1).total_seconds()
        imputed = [
            (time, [int(prop1 * a + prop2 * b) for a, b in zip(md1, md2)])
            for time in interval_times
            for prop1, prop2 in [
                (
                    1 - (tmd2 - time).total_seconds() / interval_size,
                    (tmd2 - time).total_seconds() / interval_size,
                )
            ]
        ]
        acc += imputed
        metadatawindows = metadatawindows[1:]
    return acc


def maxOptions(rows):
    """Return the maximum values from each column across multiple rows.

    Args:
        rows (list): List of rows, where each row is a list containing values for multiple columns.

    Returns:
        list: A list of maximum values for each column.
    """
    return [max(filter(None, col), default=None) for col in zip(*[r[1] for r in rows])]


def mergeDuplicates(metadatas):
    """Merge duplicate rows by date, selecting the maximum value for each column.

    Args:
        metadatas (list): List of tuples, where each tuple contains a date and metadata for that date.

    Returns:
        list: A list of tuples with merged metadata for each unique date.
    """
    grouped = defaultdict(list)
    for date, meta in metadatas:
        grouped[date].append(meta)
    return sorted((date, maxOptions(rows)) for date, rows in grouped.items())


def imputeByColumns(times, metadatas):
    """Impute metadata by columns over the given time intervals.

    Args:
        times (list): List of time intervals for which metadata needs to be imputed.
        metadatas (list): List of metadata entries for each time interval.

    Returns:
        list: A list of imputed metadata for each time interval.
    """
    metadatas_new = mergeDuplicates(metadatas)
    if all(len(x[1]) == 0 for x in metadatas_new):
        return [(time, []) for time in times]
    rowData = [[(date, val) for val in metadata] for date, metadata in metadatas_new]
    columns = list(zip(*rowData))
    return list(
        zip(times, map(list, zip(*[imprec(times, column, None) for column in columns])))
    )


def getTopEntityMatchingSearchSeeds(df_ss, df_crl):
    """Match top entities between search seeds and crawler data.

    Args:
        df_ss (pd.DataFrame): DataFrame containing search seed entities.
        df_crl (pd.DataFrame): DataFrame containing extracted entities.

    Returns:
        pd.DataFrame: DataFrame containing matched entities and their associated information.
    """
    crawlerItems = []
    for index, row in df_crl.iterrows():
        yaml_data = read_yaml(row["extracted_entities"])
        for x in yaml_data:
            if isinstance(x, dict):
                entity_type = x.get("type") or x.get("entity_type")
                text = x.get("text") or x.get("representative")
                frequency = x.get("frequency")
                crawlerItems.append([row["entity_id"], entity_type, text, frequency])

    crawlerItemsDF = pd.DataFrame(
        crawlerItems,
        columns=["entityID", "namedEntityType", "namedEntityText", "namedEntityCount"],
    )

    to_entity_matching_ss = (
        df_ss.rename(columns={"profile_id": "profileID", "name": "namedEntityText"})
        .merge(crawlerItemsDF, on="namedEntityText")
        .assign(
            rnCount=lambda df: df.groupby(["entityID", "profileID"])[
                "namedEntityCount"
            ].rank(method="first", ascending=False)
        )
        .query("rnCount == 1")
        .drop(columns=["namedEntityType", "rnCount"])
    )

    return to_entity_matching_ss


def getTotalVisitors(df_ea):
    """Calculate the total number of visitors for each profile and entity.

    Args:
        df_ea (pd.DataFrame): DataFrame containing entity analytics data.

    Returns:
        pd.DataFrame: DataFrame containing total visitors for each profile and entity.
    """
    return (
        df_ea.groupby(["profile_id", "entity_id"])["link_visitors"]
        .sum()
        .reset_index()
        .query("link_visitors > 0")
        .rename(
            columns={
                "profile_id": "profileID",
                "entity_id": "entityID",
                "link_visitors": "totalVisitors",
            }
        )
    )


def getPerWithNamedEntityCounts(df_ss, df_crl, profileEntityIDS):
    """Merge entity counts with profile and entity IDs.

    Args:
        df_ss (pd.DataFrame): DataFrame containing profile and named entity information.
        df_crl (pd.DataFrame): DataFrame containing extracted entities.
        profileEntityIDS (pd.DataFrame): DataFrame of profile and entity IDs.

    Returns:
        pd.DataFrame: DataFrame containing profile entity IDs and their corresponding named entity counts.
    """
    topExtractedEntities = getTopEntityMatchingSearchSeeds(df_ss, df_crl)
    result = profileEntityIDS.merge(
        topExtractedEntities, on=["profileID", "entityID"], how="left"
    )
    result["namedEntityCount"].fillna(np.nan, inplace=True)
    return result


def filterEntityAnalytics(df_ea):
    """Filter and clean entity analytics data by removing rows.

    Args:
        df_ea (pd.DataFrame): DataFrame containing entity analytics data.

    Returns:
        pd.DataFrame: Cleaned DataFrame with valid entity analytics data.
    """
    df_ea["timestamp"] = pd.to_datetime(df_ea["timestamp"])

    reloaded_pers = (
        df_ea[df_ea["link_visitors"].isnull()]
        .groupby(["profile_id", "entity_id"])
        .size()
        .reset_index(name="count")
    )
    reloaded_pers = reloaded_pers[reloaded_pers["count"] > 1]
    cleaned = df_ea.merge(
        reloaded_pers, on=["profile_id", "entity_id"], how="left", indicator=True
    )
    cleaned = cleaned[cleaned["_merge"] == "left_only"].drop(
        columns=["_merge", "count"]
    )
    cleaned = cleaned[cleaned["link_visitors"].notnull()]

    good_entities = (
        cleaned.groupby("entity_id").agg({"secondslag": "min"}).reset_index()
    )
    good_entities = good_entities[good_entities["secondslag"] > -86400]
    good_entities = good_entities[["entity_id"]]

    ea_table_groups = cleaned.merge(good_entities, on="entity_id")
    ea_table_groups = ea_table_groups[ea_table_groups["link_visitors"].notnull()]
    ea_table_groups = ea_table_groups[ea_table_groups["secondslag"] < 604800 * 4]
    ea_table_groups = ea_table_groups.drop(columns=["secondslag"]).sort_values(
        by=["entity_id", "profile_id", "timestamp"]
    )
    return ea_table_groups


def joinEntityAnalyticsWithLinkMetadata(df_lmd, df_ea, df_per, minDays, maxDays):
    """Join entity analytics data with link metadata and fill in missing visitor counts.

    Args:
        df_lmd (pd.DataFrame): DataFrame containing link metadata.
        df_ea (pd.DataFrame): DataFrame containing entity analytics data with visitor counts.
        df_per (pd.DataFrame): DataFrame containing profile and entity IDs.
        minDays (int): Minimum number of days to fill for missing times.
        maxDays (int): Maximum number of days to fill for missing times.

    Returns:
        pd.DataFrame: DataFrame containing joined entity analytics, metadata, and visitor counts.
    """
    df_lmd["timestamp"] = pd.to_datetime(df_lmd["timestamp"])
    df_ea["timestamp"] = pd.to_datetime(df_ea["timestamp"])

    eaTableGroups = filterEntityAnalytics(df_ea)

    metadatasGroups = (
        df_per[["entity_id", "profile_id"]]
        .merge(df_lmd, on="entity_id")
        .sort_values(by=["entity_id", "profile_id", "timestamp"])
        .groupby(["entity_id", "profile_id"])
        .apply(
            lambda x: [
                (
                    row["timestamp"],
                    row.drop(["entity_id", "profile_id", "timestamp"]).tolist(),
                )
                for idx, row in x.iterrows()
            ]
        )
        .to_dict()
    )

    eaGroups = (
        eaTableGroups.groupby(["entity_id", "profile_id"])
        .apply(lambda x: [(row.timestamp, row.link_visitors) for row in x.itertuples()])
        .to_dict()
    )
    eaTimeGroups = (
        eaTableGroups.groupby(["entity_id", "profile_id"])
        .apply(lambda x: [row.timestamp for row in x.itertuples()])
        .to_dict()
    )

    for key in eaTimeGroups.keys():
        eaTimeGroups[key] = [pd.to_datetime(ts) for ts in eaTimeGroups[key]]

    common_keys = set(metadatasGroups.keys()).intersection(eaTimeGroups.keys())

    res = {}
    for key in common_keys:
        times_filled = fillTimesDaily(eaTimeGroups[key], minDays, maxDays)
        res[key] = [
            (time, meta) for time, meta in zip(times_filled, metadatasGroups[key])
        ]

    res2 = {}
    for key in common_keys:
        time_visitors_filled = fillVisitorsTimesDaily(eaGroups[key], minDays, maxDays)
        visitors = [tv[1] for tv in time_visitors_filled]
        res2[key] = list(zip(res[key], visitors))

    ungrouped = []
    for key, value in res2.items():
        for (date, meta), vis in value:
            ungrouped.append([key[1], key[0], date, meta, vis])

    profileDF = pd.DataFrame(
        ungrouped,
        columns=["profileID", "entityID", "analyticsTimestamp", "meta", "visitors"],
    )
    entity_social_analytics_columns = [
        "profileID",
        "entityID",
        "analyticsTimestamp",
        "visitors",
        "fbLikes",
        "fbComments",
        "fbShares",
        "fbTotal",
        "fbClicks",
        "twitterRetweets",
        "googlePlusones",
        "linkedInShares",
        "twitterFavorites",
        "googleReshares",
        "googleReplies",
    ]
    for i, col in enumerate(entity_social_analytics_columns[4:]):
        profileDF[col] = profileDF["meta"].apply(
            lambda x: x[1][i] if i < len(x[1]) else np.nan
        )
    profileDF.drop(columns=["meta"], inplace=True)

    return profileDF


def aggregateDomains(df_domain, df_dom):
    """Aggregate domain information by counting occurrences of domain IDs, names, and publications.

    Args:
        df_domain (pd.DataFrame): DataFrame containing domain IDs.
        df_dom (pd.DataFrame): DataFrame containing additional domain information.

    Returns:
        pd.DataFrame: DataFrame containing aggregated domain information with counts and ranks.
    """
    publicationCounts = (
        df_domain.merge(df_dom, on="domain_id", how="left")
        .groupby("publication")
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
        .assign(runningTotal=lambda df: df["count"].cumsum())
        .assign(countRank=lambda df: df["count"].rank(method="first", ascending=False))
    )

    return (
        df_domain.merge(df_dom, on="domain_id")
        .merge(
            publicationCounts[["publication", "count", "countRank"]],
            on="publication",
            how="left",
        )
        .rename(columns={"count": "pubCount", "countRank": "pubRank"})
    )


def getRelevancePercentiles(df_per):
    """Calculate relevance percentiles for each entity in a profile, excluding owned media.

    Args:
        df_per (pd.DataFrame): DataFrame containing entity relevance data.

    Returns:
        pd.DataFrame: DataFrame with relevance percentiles for each profile and entity.
    """
    relevancePercentiles = (
        df_per.assign(relevance=lambda df: df["relevance_score"].fillna(0.0))
        .query("owned_media_flag != True")
        .sort_values(by=["entity_id", "profile_id"])
        .assign(
            relevancePercentile=lambda df: df.groupby("profile_id")["relevance"].rank(
                pct=True
            )
        )
    )
    return relevancePercentiles.drop(columns=["owned_media_flag"]).rename(
        columns={"profile_id": "profileID", "entity_id": "entityID"}
    )


def getRelevanceTable(df_per):
    """Create a relevance table by grouping relevance percentiles for each profile.

    Args:
        df_per (pd.DataFrame): DataFrame containing entity relevance data.

    Returns:
        pd.DataFrame: DataFrame containing relevance percentiles grouped by profile.
    """
    relevancePercentiles = getRelevancePercentiles(df_per)
    assoc = relevancePercentiles.groupby("profileID").apply(
        lambda x: x[["relevance", "relevancePercentile"]]
        .set_index("relevance")
        .to_dict()["relevancePercentile"]
    )
    relevanceTable = pd.DataFrame({"profileID": assoc.index, "assoc": assoc.values})
    return relevanceTable


def makeRelevanceMap(relevanceTable):
    """Create a relevance map from the relevance table, mapping profiles to relevance percentiles.

    Args:
        relevanceTable (pd.DataFrame): DataFrame containing relevance percentiles for each profile.

    Returns:
        dict: A dictionary mapping profile IDs to their relevance percentiles.
    """
    relevanceMap = {}
    for row in relevanceTable.itertuples():
        profileID, assoc = row.profileID, row.assoc
        relevanceMap[profileID] = defaultdict(float, assoc)
    return relevanceMap


def joinWithSyndicates(df_with_entity_id, df_connect):
    """Add syndicate child and parent information to entities.

    Args:
        df_with_entity_id (pd.DataFrame): DataFrame containing entity IDs.
        df_connect (pd.DataFrame): DataFrame containing syndicate connections.

    Returns:
        pd.DataFrame: DataFrame with syndicate child and parent flags added for each entity.
    """
    syndicates = df_connect.query(
        "type_cd == 3 and parent_entity_id != child_entity_id"
    )
    childSyndicateIds = (
        syndicates[["child_entity_id"]]
        .drop_duplicates()
        .rename(columns={"child_entity_id": "entityID"})
    )
    parentSyndicateIds = (
        syndicates[["parent_entity_id"]]
        .drop_duplicates()
        .rename(columns={"parent_entity_id": "entityID"})
    )
    result = df_with_entity_id.merge(
        childSyndicateIds.assign(isSyndicateChild=True), on="entityID", how="left"
    )
    result = result.merge(
        parentSyndicateIds.assign(isSyndicateParent=True), on="entityID", how="left"
    )
    result["isSyndicateChild"] = result["isSyndicateChild"].fillna(False)
    result["isSyndicateParent"] = result["isSyndicateParent"].fillna(False)
    return result


def parse_as_dataframe(int_list, name):
    """Convert a comma-separated list of integers into a DataFrame.

    Args:
        int_list (str): Comma-separated string of integers.
        name (str): Column name for the resulting DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the integers.
    """
    return pd.DataFrame(int_list.split(","), columns=[name]).astype(int)


def good_profile_ids(jdbcDFprof, mlExcludedProfiles=None, mlIncludedProfiles=None):
    """Filter profile IDs based on excluded or included profiles and return the relevant profiles.

    Args:
        jdbcDFprof (pd.DataFrame): DataFrame containing profile data.
        mlExcludedProfiles (str, optional): Comma-separated list of excluded profile IDs.
        mlIncludedProfiles (str, optional): Comma-separated list of included profile IDs.

    Returns:
        pd.DataFrame: DataFrame containing the filtered profile IDs and related information.
    """
    if mlExcludedProfiles:
        excluded_ids_df = parse_as_dataframe(mlExcludedProfiles, "profile_id")
        ir = (
            jdbcDFprof.merge(
                excluded_ids_df, on="profile_id", how="left", indicator=True
            )
            .query('_merge == "left_only"')
            .drop("_merge", axis=1)
        )
    elif mlIncludedProfiles:
        included_ids_df = parse_as_dataframe(mlIncludedProfiles, "profile_id")
        ir = jdbcDFprof.merge(included_ids_df, on="profile_id", how="inner")
    else:
        ir = jdbcDFprof.iloc[0:0]

    return ir.query("is_customer == True & analytics_profile_id.notnull()")[
        ["company_sector_id", "profile_id", "analytics_profile_id", "category_id"]
    ].rename({"profile_id": "profileID"}, axis=1)


def final_data_clean(
    profile_df5: pd.DataFrame,
    good_profids: pd.DataFrame,
    min_entity_date: str,
    max_entity_date: str,
    remove_zero_visitor: bool = False,
) -> pd.DataFrame:
    """Clean the profile data by applying various filters and transforming features.

    Args:
        profile_df5 (pd.DataFrame): DataFrame containing profile data.
        good_profids (pd.DataFrame): DataFrame containing good profile IDs.
        min_entity_date (str): Minimum date for entity timestamps.
        max_entity_date (str): Maximum date for entity timestamps.
        remove_zero_visitor (bool, optional): Whether to remove rows with zero visitors.

    Returns:
        pd.DataFrame: Cleaned and filtered DataFrame with relevant profile data.
    """

    def null_to_dummy_column(df: pd.DataFrame, column_name: str, replace_value: any):
        df[column_name + "IsNull"] = np.where(df[column_name].isnull(), 1, 0)
        return df

    profile_df5_new = profile_df5.drop(columns=["domain_id", "parent_id"])

    nofundme = profile_df5_new[
        ((profile_df5_new["v0"] != 0) | (profile_df5_new["v1"] != 0))
        & (profile_df5_new["entityTimestamp"].between(min_entity_date, max_entity_date))
    ].drop(columns=["articleType", "namedEntityText", "v0", "v1"])

    nofundme = nofundme.merge(good_profids[["profileID"]], on="profileID")
    nofundme = nofundme.drop(columns=["is_customer", "enabled"])

    tdf = nofundme.drop(
        columns=["is_category", "url", "company_name", "word_count"]
    )  # TODO: "domainVisits", was being dropped but absent

    null_rows = tdf[tdf.isnull().any(axis=1)].copy()

    for c in null_rows.columns:
        t = null_rows[c].isnull().value_counts()
        if len(t) > 1 or (len(t) == 1 and t.index[0]):
            print("warning: ")
            print(t)

    tdf = tdf.dropna()  # TODO: add back

    tdf = tdf[tdf["language"] == "en"].drop(columns=["language"])
    tdf["logvisitors"] = np.log2(tdf["visitors"] + 1)
    tdf["hasVisitors"] = (tdf["visitors"] > 0.0).astype(float)
    if remove_zero_visitor:
        tdf = tdf[tdf["visitors"] > 0]

    tdf = tdf.drop(columns=["entityURLProtocol", "profileUrlProtocol", "publication"])

    return tdf


class RemoveColumnsTransformer(BaseEstimator, TransformerMixin):
    """A custom transformer to remove specified columns from a DataFrame."""

    def __init__(self, columns_to_remove):
        self.columns_to_remove = columns_to_remove

    def fit(self, X, y=None):
        """No fitting required. Returns self.

        Args:
            X (pd.DataFrame): Input DataFrame.
            y (pd.Series, optional): Target values. Not used.

        Returns:
            self: The transformer itself.
        """
        return self

    def transform(self, X):
        """Transform the DataFrame by removing the specified columns.

        Args:
            X (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: DataFrame with the specified columns removed.
        """
        X_dropped = X.drop(
            columns=[col for col in self.columns_to_remove if col in X.columns],
            errors="ignore",
        )
        return X_dropped


class InteractionTransformer(BaseEstimator, TransformerMixin):
    """A custom transformer to create interaction features between specified columns."""

    def __init__(self, interactions):
        self.interactions = interactions

    def fit(self, X, y=None):
        """No fitting required. Returns self.

        Args:
            X (pd.DataFrame): Input DataFrame.
            y (pd.Series, optional): Target values. Not used.

        Returns:
            self: The transformer itself.
        """
        return self

    def transform(self, X):
        """Transform the DataFrame by adding interaction features.

        Args:
            X (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: DataFrame with interaction features added.
        """
        for name, cols in self.interactions:
            X[name] = X[cols].prod(axis=1)
        return X


class UnlogTransformer(BaseEstimator, TransformerMixin):
    """A custom transformer to reverse logarithmic transformation applied to predictions."""

    def fit(self, X, y=None):
        """No fitting required. Returns self.

        Args:
            X (pd.DataFrame): Input DataFrame.
            y (pd.Series, optional): Target values. Not used.

        Returns:
            self: The transformer itself.
        """
        return self

    def transform(self, X):
        """Transform the DataFrame by reversing the logarithmic transformation on predictions.

        Args:
            X (pd.DataFrame): Input DataFrame with 'logPredictions' column.

        Returns:
            pd.DataFrame: DataFrame with 'predictedVisitors' column.
        """
        X["predictedVisitors"] = np.expm1(X["logPredictions"] * np.log(2))
        return X


def add_temporal_features(X):
    """Add temporal features such as year, month, day, day of the week, and time lags.

    Args:
        X (pd.DataFrame): Input DataFrame containing 'analyticsTimestamp' and 'entityTimestamp' columns.

    Returns:
        pd.DataFrame: DataFrame with additional temporal features.
    """
    X["analyticsTimestamp"] = pd.to_datetime(X["analyticsTimestamp"])
    X["entityTimestamp"] = pd.to_datetime(X["entityTimestamp"])
    X["year"] = X["analyticsTimestamp"].dt.year
    X["month"] = X["analyticsTimestamp"].dt.monthsecondsLag
    X["dayOfMonth"] = X["analyticsTimestamp"].dt.day
    X["daysLag"] = (X["analyticsTimestamp"] - X["entityTimestamp"]).dt.days
    X["dayOfWeek"] = X["analyticsTimestamp"].dt.dayofweek + 1
    X["secondslag"] = (
        X["analyticsTimestamp"] - X["entityTimestamp"]
    ).dt.total_seconds()
    return X
