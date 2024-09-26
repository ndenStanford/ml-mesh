"""Define the Visitor Estimation trainer."""

# Standard Library
import os
import pickle

# 3rd party libraries
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.feature_store import FeatureStoreParams
from onclusiveml.tracking import TrackedModelCard, TrackedModelSettings
from onclusiveml.training.onclusive_model_trainer import OnclusiveModelTrainer

# Source
from src.utils import (
    InteractionTransformer,
    RemoveColumnsTransformer,
    UnlogTransformer,
    add_temporal_features,
    final_data_clean,
    getPerWithNamedEntityCounts,
    getRelevancePercentiles,
    getTotalVisitors,
    good_profile_ids,
    joinEntityAnalyticsWithLinkMetadata,
    joinWithSyndicates,
)


# define the VisitorEstimationTrainer as a subclass of the OnclusiveModelTrainer
class VisitorEstimationTrainer(OnclusiveModelTrainer):
    """Class for training and managing Visitor Estimation models."""

    def __init__(
        self,
        tracked_model_specs: TrackedModelSettings,
        model_card: TrackedModelCard,
        data_fetch_params: FeatureStoreParams,
    ) -> None:
        """Initialize the VisitorEstimationTrainer."""
        self.data_fetch_params = data_fetch_params
        self.dataset_df = None
        self.dataset_dict = {}
        self.logger = get_default_logger(__name__)

        super().__init__(
            tracked_model_specs=tracked_model_specs,
            model_card=model_card,
            data_fetch_params=self.data_fetch_params,
        )

    def build_dataset_dict(self) -> None:
        """Build the dataset dictionary from the fetched data."""
        self.dataset_dict[self.data_fetch_params.feature_view_name] = self.dataset_df

    def initialize_model(self) -> None:
        """Initialize the RandomForestRegressor model."""
        self.model = RandomForestRegressor(
            max_depth=10, n_estimators=20, random_state=42
        )
        self.logger.info("Model initialized: RandomForestRegressor")

    def create_training_argument(self) -> None:
        """Create training argument object."""
        self.min_window = self.model_card.model_params.min_window
        self.max_window = self.model_card.model_params.max_window
        self.excluded_profiles = self.model_card.model_params.excluded_profiles
        self.included_profiles = self.model_card.model_params.included_profiles
        self.index_features = self.model_card.model_params.index_features
        self.encode_features = self.model_card.model_params.encode_features
        self.exclude_features = self.model_card.model_params.exclude_features
        self.interact = self.model_card.model_params.interact
        self.min_entity_date = self.model_card.model_params.min_entity_date
        self.remove_zero_visitor = self.model_card.model_params.remove_zero_visitor

    def data_preprocess(self) -> None:
        """Process the dataframes."""
        # Create references to dataframes in self.dataset_dict
        df_ss = self.dataset_dict.get("search_seeds_feature_view")
        df_eclr = self.dataset_dict.get("eclr_links_feature_view")
        df_crl = self.dataset_dict.get("crawler_items_feature_view")
        df_per = self.dataset_dict.get("profile_entity_relationships_feature_view")
        df_prof = self.dataset_dict.get("profile_company_sectors_feature_view")
        df_lmd = self.dataset_dict.get("entity_links_lmd_feature_view")
        df_ea = self.dataset_dict.get("entity_ea_per_feature_view")
        df_ent = self.dataset_dict.get("entity_links_feature_view")
        df_dom = self.dataset_dict.get("domains_feature_view")
        df_connect = self.dataset_dict.get("entity_connections_feature_view")
        # Step 1: Join entity analytics with link metadata
        profileDF = joinEntityAnalyticsWithLinkMetadata(
            df_lmd, df_ea, df_per, self.min_window, self.max_window
        )
        # Step 2: Drop unnecessary fields
        profileDF = profileDF.drop(
            columns=["fbClicks", "googleReplies", "googleReshares", "twitterFavorites"]
        )
        # Step 3: Additional data processing and merging
        wordCounts = (
            df_ent[["entity_id"]]
            .drop_duplicates()
            .merge(df_crl[["entity_id", "word_count"]], on="entity_id", how="left")
            .rename(columns={"entity_id": "entityID", "word_count": "wordCount"})
        )
        relevanceScores = getRelevancePercentiles(df_per)
        distinctPersWithVisit = getTotalVisitors(df_ea).drop(columns=["totalVisitors"])
        perWithNamedEntityCounts = getPerWithNamedEntityCounts(
            df_ss, df_crl, distinctPersWithVisit
        )

        df_crl["entityURLProtocol"] = df_crl["url"].str.extract(
            r"(https?)://.*", expand=False
        )
        crawlerStatsDF = df_crl[
            ["entity_id", "word_count", "entityURLProtocol"]
        ].rename(columns={"entity_id": "entityID"})

        profileDF = (
            profileDF.merge(crawlerStatsDF, on="entityID")
            .merge(wordCounts, on="entityID")
            .merge(relevanceScores, on=["entityID", "profileID"])
            .merge(perWithNamedEntityCounts, on=["entityID", "profileID"])
        )
        # Step 4: Merging additional entity information
        entityInfo = df_ent[
            [
                "entity_id",
                "entity_timestamp",
                "pagerank",
                "type_cd",
                "article_type_cd",
                "domain_id",
                "language",
            ]
        ].rename(
            columns={
                "entity_id": "entityID",
                "entity_timestamp": "entityTimestamp",
                "pagerank": "pageRank",
                "type_cd": "type",
                "article_type_cd": "articleType",
            }
        )
        profileDF = profileDF.merge(entityInfo, on="entityID").query("articleType == 1")
        profileDF = joinWithSyndicates(profileDF, df_connect)
        # Step 5: Merge with domain data
        df_ent_dom = df_ent.merge(df_dom, on="domain_id", how="left").rename(
            columns={"entity_id": "entityID"}
        )
        profileDF4 = profileDF.sort_values(
            by=["profileID", "entityID", "analyticsTimestamp"]
        ).merge(df_ent_dom[["entityID", "publication"]], on="entityID", how="left")

        df_prof["profileUrlProtocol"] = df_prof["url"].str.extract(r"(https?)://.*")[0]
        profileDF4 = profileDF4.merge(
            df_prof.rename(columns={"profile_id": "profileID"}).drop(
                columns=["onboarding_validations", "start_date"]
            ),
            on="profileID",
            how="left",
        )
        profileDF4 = profileDF4.drop(
            columns=[
                "case_sensitive",
                "link_present_flag",
                "remove_suffix",
                "seed_type_cd",
                "relevance_score",
                "add_parent_company_name",
            ]
        )
        # Step 6: Process visitor data
        profileDF4["analyticsTimestamp"] = pd.to_datetime(
            profileDF4["analyticsTimestamp"]
        )
        profileDF4["entityTimestamp"] = pd.to_datetime(profileDF4["entityTimestamp"])
        profileDF4["daysLag"] = (
            profileDF4["analyticsTimestamp"] - profileDF4["entityTimestamp"]
        ).dt.days
        profileDF4["rn"] = profileDF4.groupby(["entityID", "profileID"])[
            "daysLag"
        ].rank(method="first")

        initVisitors = (
            profileDF4[profileDF4["rn"] <= 2]
            .sort_values(by=["profileID", "entityID", "analyticsTimestamp"])
            .pivot_table(
                index=["profileID", "entityID"],
                columns="rn",
                values="visitors",
                aggfunc="max",
                fill_value=0,
            )
            .rename(columns={1.0: "v0", 2.0: "v1"})
            .reset_index()
        )
        # Step 7: Process social media data
        socialCols = [
            "fbLikes",
            "fbComments",
            "fbShares",
            "fbTotal",
            "twitterRetweets",
            "googlePlusones",
            "linkedInShares",
        ]
        socialMaxes = (
            profileDF.groupby(["profileID", "entityID"])[socialCols]
            .max()
            .rename(columns={col: f"{col}Max" for col in socialCols})
        )
        # Step 8: Process domain link counts
        domainRegex = r"(https?://[^/]*/).*"
        matchingURLS = (
            df_eclr.merge(
                df_crl[["entity_id", "url"]].rename(columns={"url": "entity_url"}),
                on="entity_id",
            )
            .merge(df_per, on="entity_id")
            .merge(
                df_prof[["profile_id", "url"]].rename(columns={"url": "profileURL"}),
                on="profile_id",
            )
            .assign(
                profileDomainURL=lambda df: df["profileURL"].str.extract(domainRegex)[0]
            )
            .assign(linkDomainURL=lambda df: df["url"].str.extract(domainRegex)[0])
        ).rename(columns={"profile_id": "profileID", "entity_id": "entityID"})

        domainLinkCounts = (
            matchingURLS.assign(
                isProfileDomainLink=lambda df: df["profileDomainURL"].notnull()
                & (df["profileDomainURL"] == df["linkDomainURL"])
            )
            .groupby(["entityID", "profileID"])
            .agg(
                nonDomainLinkCount=pd.NamedAgg(
                    column="isProfileDomainLink", aggfunc=lambda x: (~x).sum()
                ),
                domainLinkCount=pd.NamedAgg(
                    column="isProfileDomainLink", aggfunc="sum"
                ),
            )
            .reset_index()
        )
        # Step 9: Final merge to get profileDF5
        profileDF5 = (
            profileDF4.merge(initVisitors, on=["entityID", "profileID"])
            .merge(socialMaxes, on=["entityID", "profileID"])
            .merge(domainLinkCounts, on=["entityID", "profileID"], how="left")
            .drop(columns=["rn", "daysLag"])
        )
        # Save preprocessed data in the dataset_dict for further use
        self.dataset_dict["profileDF5"] = profileDF5

        self.logger.info("Data preprocessing complete.")

    def make_pipeline(
        self, nfm, index_features, encode_features, interact, exclude_features
    ):
        """Create scikit-learn pipeline."""
        index_encode_features = list(
            set(index_features).intersection(set(encode_features))
        )
        index_only_features = list(set(index_features) - set(index_encode_features))
        encode_only_features = list(set(encode_features) - set(index_encode_features))
        temporal_features = [
            "year",
            "month",
            "daysLag",
            "dayOfWeek",
            "dayOfMonth",
            "secondsLag",
        ]

        assert len(encode_only_features) == 0
        # List of columns to remove
        columns_to_remove = list(
            set(
                [
                    "profileID",
                    "entityID",
                    "profileIDIndex",
                    "visitors",
                    "logvisitors",
                    "hasVisitors",
                    "fbLikesNotNaN",
                    "relevance",
                    "analyticsTimestamp",
                    "entityTimestamp",
                ]
            )
            - set([f"{feature}Index" for feature in index_only_features])
            - set([f"{feature}Vec" for feature in index_encode_features])
        )

        data_cols = list(set(nfm.columns) - set(columns_to_remove)) + temporal_features
        self.logger.info("Pipeline columns:", data_cols)

        temporal_transformer = FunctionTransformer(add_temporal_features)
        index_transformers = [
            (f"{feature}Index", OneHotEncoder(), [feature])
            for feature in index_features
        ]
        interaction_transformer = InteractionTransformer(interact)
        column_transformer = ColumnTransformer(
            transformers=index_transformers, remainder="passthrough"
        )

        pipeline = Pipeline(
            steps=[
                ("temporal", temporal_transformer),
                ("interactions", interaction_transformer),
                ("remove_columns", RemoveColumnsTransformer(columns_to_remove)),
                ("columns", column_transformer),
            ]
        )

        self.logger.info("Model pipeline initialzed")
        return pipeline

    def train(self) -> None:
        """Train the RandomForest model."""
        # Load the dataframes for training
        jdbcDFprof = self.dataset_dict.get("profile_company_sectors_feature_view")
        jdbcDFprof["category_id"] = 1
        profileDF5 = self.dataset_dict["profileDF5"]
        # Clean and preprocess data using helper methods
        goodProfids = good_profile_ids(
            jdbcDFprof, self.included_profiles, self.excluded_profiles
        )
        # Set time range for data
        max_entity_date = profileDF5["entityTimestamp"].max()
        # Clean the data
        cleaned_data = final_data_clean(
            profileDF5,
            goodProfids,
            self.min_entity_date,
            max_entity_date,
            self.remove_zero_visitor,
        )
        # Split data into training and testing sets
        train_data, test_data = train_test_split(
            cleaned_data, test_size=0.2, random_state=42
        )
        # Initialize pipeline and train the model
        data_pipe = make_pipeline(
            train_data,
            self.index_features,
            self.encode_features,
            self.interact,
            self.exclude_features,
        )
        # Train the model
        X_preprocessed = data_pipe.fit_transform(train_data)
        y = train_data["logvisitors"]
        # Step 2: Train the model
        self.model.fit(X_preprocessed, y)
        # Save the trained model and the preprocessing pipeline together
        self.full_pipeline = Pipeline(
            steps=[("data_pipe", data_pipe), ("model", self.model)]
        )

    def predict(self, inputs: pd.DataFrame):
        """Make predictions using the trained model."""
        # Step 1: Apply the full pipeline (preprocessing + model)
        X_preprocessed = self.full_pipeline.named_steps["data_pipe"].transform(inputs)
        predictions = self.full_pipeline.named_steps["model"].predict(X_preprocessed)
        # Step 2: Apply the UnlogTransformer to transform the predictions
        result = inputs.copy()
        result["logPredictions"] = predictions
        unlog_transformer = UnlogTransformer()
        result = unlog_transformer.transform(result)
        # Step 3: Return the unlogged predictions
        return result["predictedVisitors"]

    def save(self) -> None:
        """Save the trained pipeline."""
        # Save the model artifacts and any other required files
        model_path = os.path.join(
            self.tracked_model_specs.local_output_dir, "trained_pipeline"
        )
        with open(model_path, "wb") as f:
            pickle.dump(self.full_pipeline, f)
        print(f"Trained model pipeline saved to {model_path}")

    def __call__(self) -> None:
        """Call Method to run the training process."""
        super(VisitorEstimationTrainer, self).__call__()
        self.build_dataset_dict()
        self.data_preprocess()
        self.make_pipeline()
        self.initialize_model()
        self.train()
        self.save()
