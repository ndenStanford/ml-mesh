# Standard Library
import time

# Internal libraries
from onclusiveml.feature_store import FeastRepoBuilder

# Source
from src.settings import FeatureRegistrationParams


feature_registration_params = FeatureRegistrationParams()
feast_repo_builder = FeastRepoBuilder(feature_registration_params)
fs_handle = feast_repo_builder.fs_handle


feature_view = [
    feature_view
    for feature_view in fs_handle.list_feature_views()
    if feature_view.name == "iptc_third_level_feature_view"
][0]

features = [f"{feature_view.name}:{feature.name}" for feature in feature_view.features]

features += ["iptc_fourth_level_on_demand_feature_view:topic_4_llm"]

start = time.time()
entity_df = """SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp FROM "external"."iptc_third_level"
LIMIT 10"""

dataset_df = fs_handle.fs.get_historical_features(
    entity_df=entity_df, features=features
)
df = dataset_df.to_df()

print("=" * 20)
print("10 samples")
print(time.time() - start)
print(df.head())


feature_view = [
    feature_view
    for feature_view in fs_handle.list_feature_views()
    if feature_view.name == "iptc_first_level_feature_view"
][0]

features = [f"{feature_view.name}:{feature.name}" for feature in feature_view.features]

features += ["iptc_first_level_on_demand_feature_view:topic_1_llm"]

start = time.time()
entity_df = """SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp FROM "external"."iptc_first_level"
LIMIT 10"""

dataset_df = fs_handle.fs.get_historical_features(
    entity_df=entity_df, features=features
)
df = dataset_df.to_df()

print("=" * 20)
print("10 samples")
print(time.time() - start)
print(df.head())


feature_view = [
    feature_view
    for feature_view in fs_handle.list_feature_views()
    if feature_view.name == "iptc_second_level_feature_view"
][0]

features = [f"{feature_view.name}:{feature.name}" for feature in feature_view.features]

features += ["iptc_second_level_on_demand_feature_view:topic_2_llm"]

start = time.time()
entity_df = """SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp FROM "external"."iptc_second_level"
LIMIT 10"""

dataset_df = fs_handle.fs.get_historical_features(
    entity_df=entity_df, features=features
)
df = dataset_df.to_df()

print("=" * 20)
print("10 samples")
print(time.time() - start)
print(df.head())


feature_view = [
    feature_view
    for feature_view in fs_handle.list_feature_views()
    if feature_view.name == "iptc_third_level_feature_view"
][0]

features = [f"{feature_view.name}:{feature.name}" for feature in feature_view.features]

features += ["iptc_third_level_on_demand_feature_view:topic_3_llm"]

start = time.time()
entity_df = """SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp FROM "external"."iptc_third_level"
LIMIT 10"""

dataset_df = fs_handle.fs.get_historical_features(
    entity_df=entity_df, features=features
)
df = dataset_df.to_df()

print("=" * 20)
print("10 samples")
print(time.time() - start)
print(df.head())
