"""Settings test."""

# Source
from src.settings import FeatureRegistrationParams


def test_feature_registration_params():
    """Feature Registration Params settings test."""
    feature_registration_params = FeatureRegistrationParams()
    assert (
        feature_registration_params.feast_config_bucket == "kubeflow-feast-config-dev"
    )
    assert feature_registration_params.config_file == "feature_store.yaml"
    assert feature_registration_params.local_config_dir == "local-config-dir"
    assert feature_registration_params.entity_name == "iptc"
    assert feature_registration_params.entity_join_key == "iptc_id"
    assert feature_registration_params.feature_view_name == "iptc_feature_view"
    assert feature_registration_params.redshift_database == "sources"
    assert feature_registration_params.redshift_schema == "feast"
    assert feature_registration_params.redshift_table == "iptc"
    assert feature_registration_params.redshift_timestamp_field == "event_timestamp"
