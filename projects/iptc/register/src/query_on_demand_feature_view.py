from onclusiveml.data.feature_store import FeastRepoBuilder
from src.settings import FeatureRegistrationParams

feature_registration_params = FeatureRegistrationParams()
feast_repo_builder = FeastRepoBuilder(feature_registration_params)
fs_handle = feast_repo_builder.fs_handle

feature_view = [
        feature_view
        for feature_view in fs_handle.list_feature_views()
        if feature_view.name == "iptc_first_level_feature_view"
    ][0]

features = [
        f"{feature_view.name}:{feature.name}" for feature in feature_view.features
    ]

features += ["iptc_llm_feature_view_2:topic_1_llm"]
entity_df = """SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp FROM "feast"."iptc_first_level"
LIMIT 10"""

dataset_df = fs_handle.fs.get_historical_features(
    entity_df=entity_df, features=features
)
df = dataset_df.to_df()
print(df.head())