"""Train IPTC model."""

# Standard Library
import os

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import (  # type: ignore[attr-defined]
    CrawlerItemsDataFetchParams,
    EclrLinksDataFetchParams,
    EntityEaPerDataFetchParams,
    EntityConnectionsDataFetchParams,
    EntityLinksDataFetchParams,
    EntityLinksLmdDataFetchParams,
    ProfileCompanySectorsDataFetchParams,
    SearchSeedsDataFetchParams,
    DomainsDataFetchParams,
    ProfileEntityRelationshipsDataFetchParams,
    TrackedVEBaseModelCard,
    TrackedVEModelSpecs,
    DataFetchParams,
)

from src.trainer import VisitorEstimationTrainer

logger = get_default_logger(__name__)


def main() -> None:
    """Execute the training process."""
    model_specs = TrackedVEModelSpecs()
    model_card = TrackedVEBaseModelCard()
    data_fetch_params = DataFetchParams()
    crawler_items_data_fetch_params = CrawlerItemsDataFetchParams()
    data_fetch_params.entity_name = crawler_items_data_fetch_params.entity_name
    data_fetch_params.entity_join_key = crawler_items_data_fetch_params.entity_join_key
    data_fetch_params.redshift_table = crawler_items_data_fetch_params.redshift_table
    data_fetch_params.feature_view_name = crawler_items_data_fetch_params.feature_view_name

    trainer = VisitorEstimationTrainer(model_specs, model_card, data_fetch_params)
    trainer()

    for params in [
        EclrLinksDataFetchParams(),
        EntityConnectionsDataFetchParams(),
        EntityEaPerDataFetchParams(),
        EntityLinksLmdDataFetchParams(),
        EntityLinksDataFetchParams(),
        ProfileCompanySectorsDataFetchParams(),
        SearchSeedsDataFetchParams(),
        DomainsDataFetchParams(),
        ProfileEntityRelationshipsDataFetchParams(),
    ]:
        trainer.data_fetch_params.entity_name = params.entity_name
        trainer.data_fetch_params.entity_join_key = params.entity_join_key
        trainer.data_fetch_params.redshift_table = params.redshift_table
        trainer.data_fetch_params.feature_view_name = params.feature_view_name
        trainer()

    # Start the training and register models to neptune
    print(trainer.dataset_dict)


if __name__ == "__main__":
    main()
