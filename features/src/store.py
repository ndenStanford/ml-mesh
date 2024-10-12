"""Store."""

from feast import RepoConfig
from feast.infra.offline_stores.redshift import RedshiftOfflineStoreConfig
from feast.infra.online_stores.dynamodb import DynamoDBOnlineStoreConfig
from feast.infra.registry.sql import SqlRegistryConfig
from oml.register.settings import get_settings

settings = get_settings()

registry_config = SqlRegistryConfig(
    registry_store_type="aws",
    registry_type="sql",
    path=settings.mysql_registry_path,
)

offline_store = RedshiftOfflineStoreConfig(
    cluster_id=settings.redshift_cluster_id,
    user=settings.redshift_user,
    region=settings.redshift_cluster_region,
    database=settings.redshift_database,
    s3_staging_location=settings.redshift_s3_staging_directory,
    iam_role=settings.redshift_iam_role,
)

online_store = DynamoDBOnlineStoreConfig(region=settings.redshift_cluster_region)

repo_config = RepoConfig(
    project=settings.project,
    provider="aws",
    registry=registry_config,
    online_store=online_store,
    offline_store=offline_store,
    entity_key_serialization_version=2,
)
