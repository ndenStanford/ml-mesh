"""Train IPTC model."""

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import (  # type: ignore[attr-defined]
    CrawlerItemsDataFetchParams,
    DataFetchParams,
    DomainsDataFetchParams,
    EclrLinksDataFetchParams,
    EntityConnectionsDataFetchParams,
    EntityEaPerDataFetchParams,
    EntityLinksDataFetchParams,
    EntityLinksLmdDataFetchParams,
    ProfileCompanySectorsDataFetchParams,
    ProfileEntityRelationshipsDataFetchParams,
    SearchSeedsDataFetchParams,
    TrackedVEBaseModelCard,
    TrackedVEModelSpecs,
)
from src.trainer import VisitorEstimationTrainer


logger = get_default_logger(__name__)


def main() -> None:
    """Execute the training process."""
    model_specs = TrackedVEModelSpecs()
    model_card = TrackedVEBaseModelCard()
    data_fetch_params = DataFetchParams()

    trainer = VisitorEstimationTrainer(model_specs, model_card, data_fetch_params)

    # create the dataset dictionary
    for params in [
        CrawlerItemsDataFetchParams(),
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
        trainer.data_fetch_params.entity_df = params.entity_df
        trainer.data_fetch_params.features = params.features
        print('====================', trainer.data_fetch_params)
        trainer.build_dataset_dict()
    logger.info("Dataset dictionary creation complete.")

    # Start the training and register models to neptune
    trainer()


if __name__ == "__main__":
    main()
